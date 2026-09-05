import { generateObject } from 'ai'
import { NextResponse } from 'next/server'
import { ideasResponseSchema, MODEL } from '@/lib/schemas'
import type { Profile } from '@/lib/types'

export const maxDuration = 60

export async function POST(req: Request) {
  const { profile, prompt } = (await req.json()) as { profile: Profile; prompt?: string }

  const system = [
    'You are ProjectMentor, a senior engineer and mentor who invents concrete, buildable software project ideas.',
    'Ideas must be specific and original — never generic ("build a todo app"). Give each a real product name.',
    'Calibrate difficulty and scope to the developer\'s skill level and available time.',
    'Prefer projects that make strong portfolio pieces and teach transferable skills.',
  ].join(' ')

  const userPrompt = [
    `Developer profile:`,
    `- Skill level: ${profile.skillLevel}`,
    `- Languages/tools: ${profile.languages.join(', ') || 'unspecified'}`,
    `- Interests: ${profile.interests.join(', ') || 'unspecified'}`,
    `- Goal: ${profile.goal || 'unspecified'}`,
    `- Time available: ${profile.timeCommitment || 'unspecified'}`,
    profile.experience ? `- Notes: ${profile.experience}` : '',
    prompt ? `\nExtra direction from the developer: "${prompt}"` : '',
    '\nGenerate exactly 4 distinct project ideas spanning a range of ambition, all realistic for this profile.',
  ]
    .filter(Boolean)
    .join('\n')

  try {
    const { object } = await generateObject({
      model: MODEL,
      schema: ideasResponseSchema,
      system,
      prompt: userPrompt,
    })
    return NextResponse.json(object)
  } catch (err) {
    console.log('[v0] ideas route error:', (err as Error).message)
    return NextResponse.json({ error: 'generation_failed' }, { status: 502 })
  }
}
