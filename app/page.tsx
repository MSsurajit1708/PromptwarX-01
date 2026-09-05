import { SiteHeader } from '@/components/site-header'
import { Hero } from '@/components/landing/hero'
import { Capabilities, FooterCta, HowItWorks } from '@/components/landing/sections'

export default function HomePage() {
  return (
    <main className="min-h-dvh">
      <SiteHeader />
      <Hero />
      <HowItWorks />
      <Capabilities />
      <FooterCta />
    </main>
  )
}
