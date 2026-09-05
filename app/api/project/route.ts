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
    console.log('[ProjectMentor] Gemini project plan generation error/fallback:', (err as Error).message)

    const fallbackPlan = {
      overview: `A strategic 4-phase build plan for ${idea.title}. Focus on establishing a working skeleton early, then iteratively layering core feature logic, API integrations, and user interface polish.`,
      roadmap: [
        {
          title: 'Phase 1: Architecture & Database Design',
          durationWeeks: 2,
          summary: 'Define project scope, ER-diagrams, API route contracts, and initial project repository setup.',
          milestones: ['Design database schema', 'Initialize Git repo & Next.js/Flask structure', 'Setup environment variables']
        },
        {
          title: 'Phase 2: Core Backend REST APIs & Authentication',
          durationWeeks: 2,
          summary: 'Build core data models, JWT authentication, and business logic endpoints.',
          milestones: ['Implement user registration & login', 'Create primary CRUD endpoints', 'Write unit tests for APIs']
        },
        {
          title: 'Phase 3: Frontend UI & Interactive Dashboard Integration',
          durationWeeks: 2,
          summary: 'Connect React/Next.js dashboard components to backend APIs with real-time state updates.',
          milestones: ['Build responsive dashboard layouts', 'Integrate form validation & API error handling', 'Add loading skeletons']
        },
        {
          title: 'Phase 4: Testing, Security Hardening & Deployment',
          durationWeeks: 2,
          summary: 'Perform end-to-end integration testing, security checks, and deploy to Vercel/Render.',
          milestones: ['Run complete pytest/jest test suite', 'Configure production CORS & rate limits', 'Deploy live demo']
        }
      ],
      features: [
        { title: 'User Onboarding & Authentication', description: 'Secure registration, login, and JWT session handling.', priority: 'Must-have', effort: 'M' },
        { title: 'Core Analytics Dashboard', description: 'Interactive visual data widgets displaying real-time metrics.', priority: 'Must-have', effort: 'M' },
        { title: 'Data Export & PDF Reporting', description: 'Export project analysis and reports to PDF/CSV format.', priority: 'Nice-to-have', effort: 'S' },
        { title: 'AI Model Integration Service', description: 'Predictive intelligence pipeline connecting backend to LLM/ML models.', priority: 'Must-have', effort: 'L' },
        { title: 'Dark Mode & Responsive Mobile UI', description: 'Accessible Tailwind UI layout tailored for all screen sizes.', priority: 'Nice-to-have', effort: 'S' },
        { title: 'Automated Email Notifications', description: 'Email alerts for task deadlines and system milestones.', priority: 'Stretch', effort: 'M' }
      ],
      techStack: {
        frontend: [
          { name: 'Next.js & React', category: 'Frontend Framework', reason: 'Provides server-side rendering, fast page loads, and modern UI routing.' },
          { name: 'Tailwind CSS & shadcn/ui', category: 'Styling & UI Components', reason: 'Clean, responsive, tech-startup aesthetic out of the box.' }
        ],
        backend: [
          { name: 'Python & Flask', category: 'REST API Backend', reason: 'Lightweight, rapid API development with easy AI/ML integration.' }
        ],
        data: [
          { name: 'PostgreSQL & SQLAlchemy', category: 'Relational Database', reason: 'Relational integrity, strong typing, and schema migration support.' }
        ],
        tooling: [
          { name: 'Docker & Git', category: 'DevOps & Version Control', reason: 'Ensures reproducible builds and version tracking across team members.' }
        ]
      }
    }

    return NextResponse.json(fallbackPlan)
  }
}
