import { SiteHeader } from '@/components/site-header'
import { WorkspaceClient } from '@/components/workspace/workspace-client'

export default async function ProjectPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  return (
    <main className="min-h-dvh">
      <SiteHeader />
      <div className="mx-auto w-full max-w-4xl px-4 py-10 sm:px-6">
        <WorkspaceClient projectId={id} />
      </div>
    </main>
  )
}
