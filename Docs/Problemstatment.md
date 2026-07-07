# Problem Statement: AI-Powered Restaurant Recommendation System

**Use case:** Zomato-inspired restaurant discovery

## Overview

Build an AI-powered restaurant recommendation service that suggests restaurants based on user preferences. The system should combine structured restaurant data with a Large Language Model (LLM) to deliver personalized, human-like recommendations.

## Objective

Design and implement an application that:

- Accepts user preferences (location, budget, cuisine, ratings, and more)
- Uses a real-world restaurant dataset
- Leverages an LLM to generate personalized recommendations
- Presents clear, actionable results to the user

## System Workflow

### 1. Data Ingestion

- Load and preprocess the Zomato dataset from Hugging Face: [ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation)
- Extract relevant fields, including:
  - Restaurant name
  - Location
  - Cuisine
  - Cost
  - Rating

### 2. User Input

Collect user preferences such as:

| Preference | Examples |
|------------|----------|
| Location | Delhi, Bangalore |
| Budget | Low, medium, high |
| Cuisine | Italian, Chinese |
| Minimum rating | e.g. 4.0+ |
| Additional preferences | Family-friendly, quick service |

### 3. Integration Layer

- Filter and prepare restaurant data based on user input
- Pass structured results into an LLM prompt
- Design a prompt that helps the LLM reason over and rank options

### 4. Recommendation Engine

Use the LLM to:

- Rank restaurants by fit
- Explain why each recommendation matches the user’s preferences
- Optionally summarize the top choices

### 5. Output Display

Present top recommendations in a user-friendly format, including:

- Restaurant name
- Cuisine
- Rating
- Estimated cost
- AI-generated explanation

## Expected Outcome

A working recommendation flow: user enters preferences → data is filtered → the LLM ranks and explains options → the user sees a short list of well-justified restaurant suggestions in a **Next.js** web application.

## Technology

| Layer | Stack |
|-------|--------|
| ML pipeline | Python — Phases 1–4 (data, input, integration, OpenAI) |
| Backend API | FastAPI — Phase 6 |
| Frontend | Next.js (BiteWise AI Concierge UI) — Phase 7 |

The user-facing UI is the **BiteWise** web app built in Next.js, matching the Google Stitch mockups (sidebar layout, search form, AI loading, curated results, detail panel, empty and error states). It consumes the FastAPI backend which orchestrates the recommendation pipeline.
