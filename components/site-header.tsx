'use client'

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Logo } from '@/components/logo'
import { useStore } from '@/lib/store'

export function SiteHeader() {
  const { profile, projects } = useStore()
  const hasProfile = Boolean(profile)

  return (
    <header className="sticky top-0 z-40 border-b border-border/60 bg-background/80 backdrop-blur">
      <div className="mx-auto flex h-14 w-full max-w-6xl items-center justify-between px-4 sm:px-6">
        <Link href="/" aria-label="ProjectMentor home">
          <Logo />
        </Link>
        <nav className="flex items-center gap-1 sm:gap-2">
          {projects.length > 0 && (
            <Button asChild variant="ghost" size="sm" className="hidden sm:inline-flex">
              <Link href="/generate">My projects</Link>
            </Button>
          )}
          <Button asChild variant="ghost" size="sm">
            <Link href={hasProfile ? '/generate' : '/onboarding'}>
              {hasProfile ? 'Generate ideas' : 'Get started'}
            </Link>
          </Button>
          <Button asChild size="sm">
            <Link href={hasProfile ? '/generate' : '/onboarding'}>Open app</Link>
          </Button>
        </nav>
      </div>
    </header>
  )
}
