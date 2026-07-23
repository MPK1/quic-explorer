import { h } from "vue";
import { UButton } from "#components";
import type { TableColumn } from "@nuxt/ui";

export interface SimpleColumn {
  label: string;
  key: string;
  sortable?: boolean;
  class?: string;
}

export default function () {
  function buildColumns(columns: SimpleColumn[]): TableColumn<any>[] {
    return columns.map((col) => ({
      accessorKey: col.key,
      meta: col.class
        ? { class: { td: col.class, th: col.class } }
        : undefined,
      header: col.sortable
        ? ({ column }: any) =>
            h(UButton, {
              color: "neutral",
              variant: "ghost",
              label: col.label,
              icon: column.getIsSorted()
                ? column.getIsSorted() === "asc"
                  ? "i-lucide-arrow-up"
                  : "i-lucide-arrow-down"
                : "i-lucide-arrow-up-down",
              class: "-mx-2.5",
              onClick: () => column.toggleSorting(column.getIsSorted() === "asc"),
            })
        : col.label,
    }));
  }

  return { buildColumns };
}
