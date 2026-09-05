'use client'

import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react'
import type { ChatMessage, Feature, Idea, Profile, Project, ProjectPlan } from './types'

const STORAGE_KEY = 'projectmentor.v1'

type StoreState = {
  profile: Profile | null
  projects: Project[]
}

type StoreContextValue = StoreState & {
  hydrated: boolean
  setProfile: (profile: Profile) => void
  createProject: (idea: Idea) => Project
  getProject: (id: string) => Project | undefined
  setProjectPlan: (id: string, plan: ProjectPlan) => void
  setPlanStatus: (id: string, status: Project['planStatus']) => void
  toggleFeature: (id: string, featureId: string) => void
  addMentorMessage: (id: string, message: ChatMessage) => void
  deleteProject: (id: string) => void
  reset: () => void
}

const StoreContext = createContext<StoreContextValue | null>(null)

export function StoreProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<StoreState>({ profile: null, projects: [] })
  const [hydrated, setHydrated] = useState(false)
  const loaded = useRef(false)

  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY)
      if (raw) setState(JSON.parse(raw))
    } catch {
      // ignore corrupt storage
    }
    loaded.current = true
    setHydrated(true)
  }, [])

  useEffect(() => {
    if (!loaded.current) return
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
    } catch {
      // ignore quota errors
    }
  }, [state])

  const setProfile = useCallback((profile: Profile) => {
    setState((s) => ({ ...s, profile }))
  }, [])

  const createProject = useCallback((idea: Idea): Project => {
    const project: Project = {
      id: `p_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 6)}`,
      idea,
      createdAt: Date.now(),
      plan: null,
      planStatus: 'idle',
      mentorMessages: [],
    }
    setState((s) => ({ ...s, projects: [project, ...s.projects] }))
    return project
  }, [])

  const getProject = useCallback((id: string) => state.projects.find((p) => p.id === id), [state.projects])

  const updateProject = useCallback((id: string, patch: (p: Project) => Project) => {
    setState((s) => ({ ...s, projects: s.projects.map((p) => (p.id === id ? patch(p) : p)) }))
  }, [])

  const setProjectPlan = useCallback(
    (id: string, plan: ProjectPlan) => updateProject(id, (p) => ({ ...p, plan, planStatus: 'ready' })),
    [updateProject],
  )

  const setPlanStatus = useCallback(
    (id: string, status: Project['planStatus']) => updateProject(id, (p) => ({ ...p, planStatus: status })),
    [updateProject],
  )

  const toggleFeature = useCallback(
    (id: string, featureId: string) =>
      updateProject(id, (p) => {
        if (!p.plan) return p
        const features: Feature[] = p.plan.features.map((f) =>
          f.id === featureId ? { ...f, done: !f.done } : f,
        )
        return { ...p, plan: { ...p.plan, features } }
      }),
    [updateProject],
  )

  const addMentorMessage = useCallback(
    (id: string, message: ChatMessage) =>
      updateProject(id, (p) => ({ ...p, mentorMessages: [...p.mentorMessages, message] })),
    [updateProject],
  )

  const deleteProject = useCallback((id: string) => {
    setState((s) => ({ ...s, projects: s.projects.filter((p) => p.id !== id) }))
  }, [])

  const reset = useCallback(() => setState({ profile: null, projects: [] }), [])

  const value = useMemo<StoreContextValue>(
    () => ({
      ...state,
      hydrated,
      setProfile,
      createProject,
      getProject,
      setProjectPlan,
      setPlanStatus,
      toggleFeature,
      addMentorMessage,
      deleteProject,
      reset,
    }),
    [
      state,
      hydrated,
      setProfile,
      createProject,
      getProject,
      setProjectPlan,
      setPlanStatus,
      toggleFeature,
      addMentorMessage,
      deleteProject,
      reset,
    ],
  )

  return <StoreContext.Provider value={value}>{children}</StoreContext.Provider>
}

export function useStore() {
  const ctx = useContext(StoreContext)
  if (!ctx) throw new Error('useStore must be used within StoreProvider')
  return ctx
}
