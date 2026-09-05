import type { Idea, ProjectPlan } from './types'

export const LANGUAGE_OPTIONS = [
  'JavaScript',
  'TypeScript',
  'Python',
  'Go',
  'Rust',
  'Java',
  'C#',
  'Swift',
  'Kotlin',
  'SQL',
]

export const INTEREST_OPTIONS = [
  'Web apps',
  'Mobile',
  'AI / ML',
  'Developer tools',
  'Games',
  'Data & analytics',
  'Fintech',
  'Health',
  'Productivity',
  'Social',
  'E-commerce',
  'Automation',
]

export const TIME_OPTIONS = [
  'A weekend',
  '~5 hrs / week',
  '~10 hrs / week',
  'Full-time sprint',
]

export const GOAL_OPTIONS = [
  'Build a portfolio piece',
  'Learn a new skill',
  'Launch a side business',
  'Prep for interviews',
  'Contribute to open source',
  'Just for fun',
]

// Deterministic fallback used only if the AI request fails, so the demo never dead-ends.
export const FALLBACK_IDEAS: Idea[] = [
  {
    id: 'fallback-1',
    title: 'FocusForge',
    tagline: 'A distraction-aware Pomodoro timer that learns your rhythm',
    description:
      'A productivity timer that adapts session lengths based on how often you break focus, with a clean analytics view of your deep-work trends over time.',
    difficulty: 'Beginner',
    domain: 'Productivity',
    estimatedWeeks: 3,
    whyMatch:
      'Small enough to finish, but touches state management, charts, and local persistence — a great portfolio piece.',
    coreConcepts: ['State machines', 'Local storage', 'Data visualization'],
    tags: ['Web app', 'Solo', 'Frontend-heavy'],
  },
  {
    id: 'fallback-2',
    title: 'PR Digest',
    tagline: 'An AI teammate that summarizes your repo activity every morning',
    description:
      'A service that connects to a Git provider, summarizes merged pull requests and open issues, and posts a concise daily digest to your inbox or chat.',
    difficulty: 'Intermediate',
    domain: 'Developer tools',
    estimatedWeeks: 5,
    whyMatch:
      'Combines API integrations, scheduled jobs, and LLM summarization — exactly the full-stack breadth interviewers look for.',
    coreConcepts: ['Webhooks', 'Cron jobs', 'LLM summarization'],
    tags: ['Full-stack', 'Automation', 'API'],
  },
  {
    id: 'fallback-3',
    title: 'MapMyStack',
    tagline: 'Visualize any codebase as an interactive dependency map',
    description:
      'A tool that parses a project and renders an interactive graph of modules and their dependencies, letting you spot tight coupling and dead code at a glance.',
    difficulty: 'Advanced',
    domain: 'Developer tools',
    estimatedWeeks: 8,
    whyMatch:
      'Ambitious and technical: parsing, graph layout, and performance work that stands out in a senior portfolio.',
    coreConcepts: ['AST parsing', 'Graph layout', 'Performance'],
    tags: ['Visualization', 'Advanced', 'Tooling'],
  },
]

export function fallbackPlan(idea: Idea): ProjectPlan {
  return {
    overview: `A pragmatic plan to build ${idea.title}. Start narrow with a working core, then layer on polish and stretch features once the fundamentals feel solid.`,
    roadmap: [
      {
        title: 'Foundations',
        durationWeeks: 1,
        summary: 'Set up the project, scaffolding, and a walking skeleton you can run end to end.',
        milestones: ['Initialize the repo and tooling', 'Build the core data model', 'Ship a minimal working screen'],
      },
      {
        title: 'Core feature',
        durationWeeks: Math.max(1, Math.round(idea.estimatedWeeks / 2)),
        summary: 'Implement the main value of the app and make it genuinely usable.',
        milestones: ['Build the primary workflow', 'Persist real data', 'Handle the obvious edge cases'],
      },
      {
        title: 'Polish & ship',
        durationWeeks: Math.max(1, idea.estimatedWeeks - Math.round(idea.estimatedWeeks / 2) - 1),
        summary: 'Refine the experience, write a README, and deploy it somewhere public.',
        milestones: ['Refine the UI and empty states', 'Write docs and a demo', 'Deploy and share'],
      },
    ],
    features: [
      { id: 'f1', title: 'Core workflow', description: 'The single most important thing the app does.', priority: 'Must-have', effort: 'L', done: false },
      { id: 'f2', title: 'Data persistence', description: 'Save and reload user data reliably.', priority: 'Must-have', effort: 'M', done: false },
      { id: 'f3', title: 'Onboarding / empty states', description: 'Guide a brand-new user to their first win.', priority: 'Nice-to-have', effort: 'S', done: false },
      { id: 'f4', title: 'Analytics dashboard', description: 'Give users insight into their own usage.', priority: 'Nice-to-have', effort: 'M', done: false },
      { id: 'f5', title: 'Public sharing', description: 'Let users share their results with a link.', priority: 'Stretch', effort: 'M', done: false },
    ],
    techStack: {
      frontend: [
        { name: 'Next.js', category: 'Framework', reason: 'Full-stack React with routing and server actions in one place.' },
        { name: 'Tailwind CSS', category: 'Styling', reason: 'Fast, consistent styling without leaving your markup.' },
      ],
      backend: [
        { name: 'Route Handlers', category: 'API', reason: 'Colocate your API with the app; no separate server to manage.' },
      ],
      data: [
        { name: 'Postgres', category: 'Database', reason: 'A dependable relational store that scales with the project.' },
      ],
      tooling: [
        { name: 'TypeScript', category: 'Language', reason: 'Catch mistakes early and document your data shapes.' },
        { name: 'Vercel', category: 'Hosting', reason: 'Deploy from Git with zero config.' },
      ],
    },
  }
}
