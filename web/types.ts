export interface Implementation {
    uuid: string
    name: string
    maintainer: string
    language: string
    repo_url: string
    logo_url?: string
    created_at: string
    created_by: string
    updated_at?: string
    updated_by?: string
    invalidated_at?: string
    invalidated_by?: string
    invalidation_reason?: string
}

export interface Feature {
    uuid: string
    name: string
    short_name: string
    description: string
    value_type: string
    value_meta?: object | null
    created_at: string
    created_by: string
    updated_at?: string
    updated_by?: string
}

export interface Entry {
    implementation_uuid: string
    feature_uuid: string
    value: string | number | boolean | object | Array<any>
    comment?: string
    source: string
    source_url?: string
    created_at: string
    created_by: string
    updated_at?: string
    updated_by?: string
}

export interface GithubRepo {
    stargazers_count: number
    forks_count: number
    created_at: string
}
