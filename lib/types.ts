export type SkillLevel = 'beginner' | 'intermediate' | 'advanced'

export type Profile = {
  skillLevel: SkillLevel
  languages: string[]
  interests: string[]
  goal: string
  timeCommitment: string
  experience: string
}

export type Difficulty = 'Beginner' | 'Intermediate' | 'Advanced'

export type Idea = {
  id: string
  title: string
  tagline: string
  description: string
  difficulty: Difficulty
  domain: string
  estimatedWeeks: number
  whyMatch: string
  coreConcepts: string[]
  tags: string[]
}

export type RoadmapPhase = {
  title: string
  durationWeeks: number
  summary: string
  milestones: string[]
}

export type Feature = {
  id: string
  title: string
  description: string
  priority: 'Must-have' | 'Nice-to-have' | 'Stretch'
  effort: 'S' | 'M' | 'L'
  done: boolean
}

export type TechChoice = {
  name: string
  category: string
  reason: string
}

export type TechStack = {
  frontend: TechChoice[]
  backend: TechChoice[]
  data: TechChoice[]
  tooling: TechChoice[]
}

export type ProjectPlan = {
  overview: string
  roadmap: RoadmapPhase[]
  features: Feature[]
  techStack: TechStack
}

export type ChatMessage = {
  id: string
  role: 'user' | 'assistant'
  content: string
}

export type Project = {
  id: string
  idea: Idea
  createdAt: number
  plan: ProjectPlan | null
  planStatus: 'idle' | 'loading' | 'ready' | 'error'
  mentorMessages: ChatMessage[]
}
