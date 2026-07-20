import type { Entry } from "~/types";

export interface FeatureFilter {
  label: string;
  feature: string;
  mode: "value" | "value-or-unset" | "set";
  value_type: string;
  value: any;
  arraymode?: "contains-one" | "contains-all";
}

function matchesFilter(entry: Entry | undefined, filter: FeatureFilter): boolean {
  switch (filter.value_type) {
    case "boolean":
      switch (filter.mode) {
        case "value-or-unset":
          return !entry || entry.value === filter.value;
        case "value":
          return !!entry && entry.value === filter.value;
        case "set":
          return (!!entry && filter.value) || (!entry && !filter.value);
      }
    case "array":
      switch (filter.mode) {
        case "value-or-unset":
          if (!entry) return true;
        case "value":
          if (!entry) return false;
          if (filter.arraymode === "contains-all") {
            return filter.value.every((v: any) =>
              (entry.value as any[]).includes(v),
            );
          } else if (filter.arraymode === "contains-one") {
            return filter.value.some((v: any) =>
              (entry.value as any[]).includes(v),
            );
          }
          return false;
        case "set":
          return (!!entry && filter.value) || (!entry && !filter.value);
      }
    default:
      return true;
  }
}

export default function () {
  function filterByFeatures<T extends { uuid: string }>(
    rows: T[],
    entries: Entry[],
    filters: FeatureFilter[],
  ): T[] {
    if (!filters.length) return rows;
    return rows.filter((row) =>
      filters.every((filter) => {
        const entry = entries.find(
          (e) =>
            e.implementation_uuid === row.uuid &&
            e.feature_uuid === filter.feature,
        );
        return matchesFilter(entry, filter);
      }),
    );
  }

  return { matchesFilter, filterByFeatures };
}
