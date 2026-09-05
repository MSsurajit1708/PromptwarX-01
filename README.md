# ProjectMentor AI

ProjectMentor AI is a modern, AI-powered web platform that helps final-year college/university students discover practical project ideas based on their interests, skills, academic background, career goals, preferred technologies, and difficulty level.

## Architecture Overview

The application uses a unified, full-stack architecture built on Next.js (App Router):

*   **Frontend**: Next.js, React, Tailwind CSS, shadcn/ui.
*   **Backend**: Next.js API Routes (`app/api/*`).
*   **Database**: PostgreSQL managed via Prisma ORM.
*   **AI Integration**: Abstracted AI Service layer (`lib/services/ai-service.ts`) ready to connect to Google Gemini, OpenAI, etc.
*   **Authentication**: NextAuth.js (Session/JWT based).

## Folder Structure

```
project-mentor-ai/
├── app/                  # Next.js App Router (Frontend Pages & Backend APIs)
│   ├── api/              # Backend API Routes
│   │   ├── auth/         # Authentication endpoints
│   │   ├── profile/      # User profile management
│   │   ├── projects/     # Project generation, analysis, features APIs
│   │   └── tasks/        # Task management APIs
│   ├── dashboard/        # Student dashboard page
│   ├── generate/         # Project generation flow
│   ├── projects/         # Project workspace & details
│   └── page.tsx          # Landing page
├── components/           # React Components (UI, forms, layouts)
├── lib/                  # Shared utilities and services
│   └── services/         # Business logic (e.g., ai-service.ts)
├── prisma/               # Database ORM configuration
│   └── schema.prisma     # Database schema (Users, Projects, Profiles, Tasks)
└── public/               # Static assets
```

## Setup Instructions

Since Node.js is required to run this project, please follow these steps:

1.  **Install Node.js**: Download and install from [nodejs.org](https://nodejs.org/).
2.  **Install Dependencies**: Run `npm install` in the project root.
3.  **Database Setup**: 
    *   Install PostgreSQL.
    *   Create a `.env` file in the root directory and add your connection string:
        `DATABASE_URL="postgresql://user:password@localhost:5432/projectmentor"`
4.  **Prisma Migrations**: Run `npx prisma db push` to create the tables in your database.
5.  **Environment Variables**: Add your AI API key to the `.env` file (e.g., `GEMINI_API_KEY="your-key"`).
6.  **Run Development Server**: Run `npm run dev` and navigate to `http://localhost:3000`.

## Implemented So Far (Stage 1)

*   **Database Schema**: Defined in `prisma/schema.prisma` (Users, Profiles, Projects, Tasks).
*   **API Routes**: Folder structure established under `app/api/`.
*   **AI Service Mock**: Created `lib/services/ai-service.ts` to show the prompt engine abstraction.
*   **Sample API Endpoint**: Implemented `app/api/projects/generate/route.ts` as a starting point for project generation.

Please refer to the `implementation_plan.md` artifact for the remaining roadmap.
