import { generateObject } from 'ai'
import { NextResponse } from 'next/server'
import { MODEL, planSchema } from '@/lib/schemas'
import type { Idea, Profile } from '@/lib/types'

export const maxDuration = 60

export async function POST(req: Request) {
  const { idea, profile } = (await req.json()) as { idea: Idea; profile: Profile | null }

  const system = [
    'You are ProjectMentor, a pragmatic senior engineer creating a concrete build plan for a specific project.',
    'Be realistic and actionable. Roadmap phases should build on each other from a walking skeleton to a shippable product.',
    'Feature list should be prioritized honestly — most things are Nice-to-have or Stretch, only a few are Must-have.',
    'Tech stack recommendations must fit the developer\'s known languages when possible, with a short concrete reason each.',
  ].join(' ')

  const prompt = [
    `Project: ${idea.title} — ${idea.tagline}`,
    `Description: ${idea.description}`,
    `Difficulty: ${idea.difficulty}. Estimated ${idea.estimatedWeeks} weeks. Domain: ${idea.domain}.`,
    profile
      ? `Developer: ${profile.skillLevel}, knows ${profile.languages.join(', ') || 'general tooling'}, has ${profile.timeCommitment || 'some time'} per week.`
      : '',
    '\nProduce a complete build plan: a strategic overview, a phased roadmap, a prioritized feature backlog, and a recommended tech stack.',
  ]
    .filter(Boolean)
    .join('\n')

  try {
    const { object } = await generateObject({
      model: MODEL,
      schema: planSchema,
      system,
      prompt,
    })
    return NextResponse.json(object)
  } catch (err) {
    console.log('[v0] project route error:', (err as Error).message)
    return NextResponse.json({ error: 'generation_failed' }, { status: 502 })
  }
}
