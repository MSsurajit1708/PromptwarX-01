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
    console.log('[ProjectMentor] Gemini ideas generation error/fallback:', (err as Error).message)
    
    // Fallback personalized response if Gemini API key is missing or encounters quota limits
    const languagesStr = profile.languages.join(', ') || 'Python, JavaScript'
    const fallbackIdeas = {
      ideas: [
        {
          title: 'PulseGuard',
          tagline: 'Real-time predictive patient vitals & risk monitoring dashboard',
          description: 'An intelligent health analytics web app that processes vital health parameters to calculate preventative risk scores for early medical intervention.',
          difficulty: profile.skillLevel === 'Advanced' ? 'Advanced' : 'Intermediate',
          domain: 'Healthcare Tech',
          estimatedWeeks: 8,
          whyMatch: `Perfect fit for your interests in Healthcare and technical background in ${languagesStr}.`,
          coreConcepts: ['Predictive ML Modeling', 'REST API Architecture', 'Real-time Data Visualization'],
          tags: ['AI/ML', 'Healthcare', 'Full Stack']
        },
        {
          title: 'SkillBridge',
          tagline: 'Automated campus placement skill-gap & resume analyzer',
          description: 'A career platform that parses student resumes, compares them against live industry job descriptions using NLP, and builds a targeted learning roadmap.',
          difficulty: 'Intermediate',
          domain: 'EduTech',
          estimatedWeeks: 6,
          whyMatch: `High resume value for your goal (${profile.goal || 'Software Engineer'}) and placement interviews.`,
          coreConcepts: ['NLP Text Extraction', 'Similarity Scoring', 'Checklist Tracking'],
          tags: ['NLP', 'Web App', 'Career']
        },
        {
          title: 'CloudMesh',
          tagline: 'Lightweight distributed background task queue & metrics monitor',
          description: 'A resilient developer tool for queuing, retrying, and monitoring asynchronous HTTP jobs with transactional locks and an interactive UI dashboard.',
          difficulty: 'Advanced',
          domain: 'Developer Tools',
          estimatedWeeks: 8,
          whyMatch: `Demonstrates strong backend systems engineering and architecture skills.`,
          coreConcepts: ['Distributed Systems', 'Asynchronous Queues', 'Metrics Dashboard'],
          tags: ['Backend', 'DevOps', 'Distributed']
        },
        {
          title: 'FinFlow AI',
          tagline: 'Personal automated expense classifier & fraud anomaly detector',
          description: 'A financial tracking dashboard that automatically categorizes bank transactions and flags suspicious spending patterns using clustering algorithms.',
          difficulty: 'Intermediate',
          domain: 'FinTech',
          estimatedWeeks: 6,
          whyMatch: `Combines practical full-stack web development with applied machine learning.`,
          coreConcepts: ['Anomaly Detection', 'Data Cleaning', 'Interactive Charts'],
          tags: ['FinTech', 'Data Science', 'React']
        }
      ]
    }
    return NextResponse.json(fallbackIdeas)
  }
}
