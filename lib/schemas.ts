import { createGoogleGenerativeAI } from '@ai-sdk/google'
import { z } from 'zod'

const apiKey =
  process.env.AI_API_KEY ||
  process.env.GEMINI_API_KEY ||
  process.env.GOOGLE_GENERATIVE_AI_API_KEY ||
  ''

export const googleProvider = createGoogleGenerativeAI({
  apiKey,
})

export const MODEL = googleProvider('gemini-1.5-flash')

export const ideaSchema = z.object({
  title: z.string().describe('A short, memorable product name (1-3 words).'),
  tagline: z.string().describe('A punchy one-line pitch, under 90 characters.'),
  description: z.string().describe('2-3 sentences describing what the project is and does.'),
  difficulty: z.enum(['Beginner', 'Intermediate', 'Advanced']),
  domain: z.string().describe('The primary category, e.g. "Developer tools".'),
  estimatedWeeks: z.number().int().min(1).max(16).describe('Realistic weeks to a shippable version.'),
  whyMatch: z.string().describe('One sentence on why this fits the developer\'s profile.'),
  coreConcepts: z.array(z.string()).min(2).max(4).describe('Key technical concepts they will practice.'),
  tags: z.array(z.string()).min(2).max(4),
})

export const ideasResponseSchema = z.object({
  ideas: z.array(ideaSchema).length(4),
})

export const planSchema = z.object({
  overview: z.string().describe('A 2-3 sentence strategic summary of how to approach the build.'),
  roadmap: z
    .array(
      z.object({
        title: z.string(),
        durationWeeks: z.number().int().min(1).max(8),
        summary: z.string(),
        milestones: z.array(z.string()).min(2).max(4),
      }),
    )
    .min(3)
    .max(5),
  features: z
    .array(
      z.object({
        title: z.string(),
        description: z.string(),
        priority: z.enum(['Must-have', 'Nice-to-have', 'Stretch']),
        effort: z.enum(['S', 'M', 'L']),
      }),
    )
    .min(5)
    .max(8),
  techStack: z.object({
    frontend: z.array(z.object({ name: z.string(), category: z.string(), reason: z.string() })).min(1).max(3),
    backend: z.array(z.object({ name: z.string(), category: z.string(), reason: z.string() })).min(1).max(3),
    data: z.array(z.object({ name: z.string(), category: z.string(), reason: z.string() })).min(1).max(2),
    tooling: z.array(z.object({ name: z.string(), category: z.string(), reason: z.string() })).min(1).max(3),
  }),
})
