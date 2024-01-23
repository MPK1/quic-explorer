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

export interface GithubRepo {
    stargazers_count: number
    forks_count: number
    created_at: string
}