# UI/UX DESIGN SYSTEM SPECIFICATION
## AI Workforce — Autonomous Business Workflow Automation Platform
**Document Identifier:** UIX-AIWF-2026-001  
**Version:** 1.0.0 | **Status:** FINAL & APPROVED  
**Target Framework:** React 18+ (TypeScript), Radix UI, Tailwind CSS & CSS Custom Properties  
**Accessibility Target:** WCAG 2.1 AA Compliance  

---

## TABLE OF CONTENTS
1. [Design Philosophy & Core Aesthetics](#1-design-philosophy--core-aesthetics)
2. [Global CSS Architecture & Design Tokens](#2-global-css-architecture--design-tokens)
   - 2.1 [Color Tokens (Dark & Light Modes)](#21-color-tokens-dark--light-modes)
   - 2.2 [Typography System](#22-typography-system)
   - 2.3 [Spacing, Radius & Elevation Tokens](#23-spacing-radius--elevation-tokens)
   - 2.4 [Z-Index & Transition Tokens](#24-z-index--transition-tokens)
3. [Global Component Hierarchy & Reusable Primitives](#3-global-component-hierarchy--reusable-primitives)
   - 3.1 [Application Shell & Layout System](#31-application-shell--layout-system)
   - 3.2 [Feedback & Dialog System (Modals, Drawers, Toasts)](#32-feedback--dialog-system-modals-drawers-toasts)
   - 3.3 [Data Display (Tables, Pagination, Cards)](#33-data-display-tables-pagination-cards)
   - 3.4 [Form Controls & Validation States](#34-form-controls--validation-states)
   - 3.5 [Universal State Primitives (Loading, Empty, Error, Skeleton)](#35-universal-state-primitives-loading-empty-error-skeleton)
   - 3.6 [Navigation & Command Palette (`Cmd+K`)](#36-navigation--command-palette-cmdk)
4. [Specialized Platform Views & Domain Components](#4-specialized-platform-views--domain-components)
   - 4.1 [Executive Dashboard](#41-executive-dashboard)
   - 4.2 [AI Agent Studio & Prompt Configuration](#42-ai-agent-studio--prompt-configuration)
   - 4.3 [Visual Workflow Builder (React Flow Canvas)](#43-visual-workflow-builder-react-flow-canvas)
   - 4.4 [Custom Workflow Node System](#44-custom-workflow-node-system)
   - 4.5 [Human-in-the-Loop Approval Center & Review Drawer](#45-human-in-the-loop-approval-center--review-drawer)
   - 4.6 [Execution Timeline & Waterfall Trace Viewer](#46-execution-timeline--waterfall-trace-viewer)
   - 4.7 [Knowledge Base & Chunk Inspection UI](#47-knowledge-base--chunk-inspection-ui)
   - 4.8 [Tool & MCP Server Registry](#48-tool--mcp-server-registry)
5. [Responsive Breakpoints & Accessibility Standards](#5-responsive-breakpoints--accessibility-standards)

---

## 1. DESIGN PHILOSOPHY & CORE AESTHETICS

The **AI Workforce** interface is designed for high-density enterprise operations, blending deep configurability with fluid visual workflows. 
- **Aesthetic Direction**: Sleek modern enterprise dark-mode primary, with seamless light-mode support. Subtle glassmorphism, refined micro-borders (`1px solid var(--border-subtle)`), deterministic typography, and purposeful state animations.
- **Cognitive Clarity**: Workflow nodes, risk levels, and execution statuses use consistent semantic colors across all screens to ensure immediate situational awareness.
- **Modularity**: Zero ad-hoc, page-specific CSS classes. All UI views are constructed from a central set of Radix UI primitives styled with canonical design tokens.

---

## 2. GLOBAL CSS ARCHITECTURE & DESIGN TOKENS

### 2.1 Color Tokens (Dark & Light Modes)

```css
:root {
  /* ── Light Mode Color Tokens ── */
  --bg-app: #f8fafc;
  --bg-surface: #ffffff;
  --bg-surface-elevated: #f1f5f9;
  --bg-surface-hover: #e2e8f0;

  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-muted: #94a3b8;
  --text-inverse: #ffffff;

  --border-subtle: #e2e8f0;
  --border-medium: #cbd5e1;
  --border-strong: #94a3b8;

  --brand-primary: #2563eb;
  --brand-primary-hover: #1d4ed8;
  --brand-subtle: #eff6ff;

  /* Semantic Status Tokens */
  --status-pending: #64748b;
  --status-running: #2563eb;
  --status-waiting: #d97706; /* Amber for Approval */
  --status-completed: #059669; /* Emerald */
  --status-failed: #dc2626; /* Crimson */
  --status-cancelled: #475569;

  /* Risk Level Tokens */
  --risk-low: #059669;
  --risk-medium: #d97706;
  --risk-high: #dc2626;
  --risk-critical: #7c2d12;
}

[data-theme='dark'] {
  /* ── Dark Mode Color Tokens (Default Enterprise Theme) ── */
  --bg-app: #090d16;
  --bg-surface: #0f172a;
  --bg-surface-elevated: #1e293b;
  --bg-surface-hover: #334155;

  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --text-inverse: #0f172a;

  --border-subtle: #1e293b;
  --border-medium: #334155;
  --border-strong: #475569;

  --brand-primary: #3b82f6;
  --brand-primary-hover: #60a5fa;
  --brand-subtle: #172554;

  /* Semantic Status Tokens */
  --status-pending: #94a3b8;
  --status-running: #60a5fa;
  --status-waiting: #f59e0b;
  --status-completed: #10b981;
  --status-failed: #ef4444;
  --status-cancelled: #64748b;

  /* Risk Level Tokens */
  --risk-low: #10b981;
  --risk-medium: #f59e0b;
  --risk-high: #ef4444;
  --risk-critical: #f87171;
}
```

### 2.2 Typography System

- **Primary Font Family**: `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Code & Monospace Font Family**: `'JetBrains Mono', 'Fira Code', Menlo, monospace`

| Token | Size (rem / px) | Line Height | Weight | Usage |
|---|---|---|---|---|
| `--text-xs` | 0.75rem (12px) | 1.0rem | 400 / 500 | Badges, timestamps, node metadata |
| `--text-sm` | 0.875rem (14px) | 1.25rem | 400 / 500 | Body text, table cells, form labels |
| `--text-base` | 1.0rem (16px) | 1.5rem | 400 / 500 | Primary UI buttons, card content |
| `--text-lg` | 1.125rem (18px) | 1.75rem | 600 | Card headings, drawer titles |
| `--text-xl` | 1.25rem (20px) | 1.75rem | 600 | Modal headings, section headers |
| `--text-2xl` | 1.5rem (24px) | 2.0rem | 700 | Main page titles, dashboard metrics |
| `--text-3xl` | 1.875rem (30px) | 2.25rem | 800 | Top-level summary headers |

### 2.3 Spacing, Radius & Elevation Tokens

```css
:root {
  /* Spacing Scale */
  --space-1: 0.25rem; /* 4px */
  --space-2: 0.5rem;  /* 8px */
  --space-3: 0.75rem; /* 12px */
  --space-4: 1.0rem;  /* 16px */
  --space-6: 1.5rem;  /* 24px */
  --space-8: 2.0rem;  /* 32px */
  --space-12: 3.0rem; /* 48px */

  /* Border Radii */
  --radius-sm: 0.25rem;  /* 4px - Inputs, badges */
  --radius-md: 0.375rem; /* 6px - Buttons, select menus */
  --radius-lg: 0.5rem;   /* 8px - Cards, dialogs */
  --radius-xl: 0.75rem;  /* 12px - Workflow nodes */
  --radius-full: 9999px; /* Avatars, pill tags */

  /* Elevation Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-modal: 0 20px 25px -5px rgba(0, 0, 0, 0.25), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}
```

### 2.4 Z-Index & Transition Tokens

```css
:root {
  --z-canvas: 1;
  --z-sticky-nav: 50;
  --z-dropdown: 100;
  --z-drawer: 200;
  --z-modal: 300;
  --z-toast: 400;
  --z-tooltip: 500;

  --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-normal: 250ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

---

## 3. GLOBAL COMPONENT HIERARCHY & REUSABLE PRIMITIVES

### 3.1 Application Shell & Layout System
- **Sidebar**: Collapsible (64px icon rail or 240px expanded) containing Logo, Organization Selector, Primary Navigation (Dashboard, Workflows, Agents, Knowledge, Approvals, Runs, Observability, Settings).
- **Header**: Fixed height (56px) displaying breadcrumbs, Global Search / Command Palette shortcut (`Cmd+K`), Environment Badge (`Production` / `Staging`), Pending Approvals counter, and User Profile menu.
- **Content Area**: Flexible container with responsive margins (`p-6` on desktop, `p-4` on tablet).

### 3.2 Feedback & Dialog System
- **Modal Dialog (`<Modal />`)**: Centered overlay on backdrop (`rgba(0,0,0,0.6)` with blur). Used for critical confirmations, new agent wizard, and credentials input.
- **Slide-over Drawer (`<Drawer />`)**: 640px wide right-hand drawer for high-density editing (Node Inspector, Step Run Details, Approval Review Drawer).
- **Toast Notifications (`<Toast />`)**: Bottom-right floating toasts with auto-dismiss (4s). Variants: `info`, `success`, `warning`, `error`.

### 3.3 Data Display
- **Data Table (`<DataTable />`)**: Virtualized table supporting column sorting, multi-attribute filtering, row selection, sticky headers, and pagination footer.
- **Metric Card (`<MetricCard />`)**: Displays numeric KPI, trend badge (e.g. `+14.2%`), icon, and mini sparkline.

### 3.4 Form Controls & Validation States
- **Input / Textarea**: Floating or top-aligned labels, monospace code toggle, character counter, and instant inline validation message with error boundary styling.
- **Select / Combobox**: Searchable dropdowns with keyboard arrow navigation and virtual scrolling for large option lists.

### 3.5 Universal State Primitives
- **Loading Skeleton (`<Skeleton />`)**: Pulsing light/dark gradient matching target typography and card layouts.
- **Empty State (`<EmptyState />`)**: Illustration, title, descriptive subtext, and clear call-to-action button.
- **Error Boundary View (`<ErrorState />`)**: User-friendly crash explanation, stack trace toggle (dev only), and "Reload View" button.
- **Permission Denied (`<ForbiddenState />`)**: Lock icon, explanation of missing RBAC privilege, and contact administrator action.

### 3.6 Navigation & Command Palette (`Cmd+K`)
Global keyboard navigation modal supporting fuzzy search over:
- Workflows (`/workflows/...`)
- Agents (`/agents/...`)
- Pending Approvals (`/approvals/...`)
- Quick Actions: *Create Agent*, *Create Workflow*, *Upload Document*.

---

## 4. SPECIALIZED PLATFORM VIEWS & DOMAIN COMPONENTS

### 4.1 Executive Dashboard
- **Top Row KPI Tiles**: Total Executions (MTD), Success Rate (%), Token Expenditure ($), Pending Human Approvals.
- **Main Section**: Real-time execution volume chart (Recharts bar/line chart) + Recent Workflow Runs table.
- **Right Sidebar**: Approval Queue inbox featuring pending actions ordered by timeout expiration.

### 4.2 AI Agent Studio & Prompt Configuration
- **Split-Screen Layout**:
  - *Left Panel (Configuration)*: Agent identity, Model selector dropdown, Temperature slider, System prompt editor (with token counter and auto-expanding textarea), Tool binding checkboxes, Knowledge Base bindings.
  - *Right Panel (Interactive Playground)*: Chat interface to run sandboxed test queries against the draft agent version before publishing.

### 4.3 Visual Workflow Builder (React Flow Canvas)
- **Canvas Toolbar**: Drag-and-drop node palette (Trigger, Agent, Tool, Approval, Condition, Finish), Zoom controls, Mini-map, Auto-layout button (Dagre/ELK), Undo/Redo, Publish button.
- **Grid Background**: Subtle dot grid (`16px` pitch) with snapping.
- **Interactive Connections**: Bezier curve edges with animated flow particles during active runs.

### 4.4 Custom Workflow Node System

```
┌────────────────────────────────────────────────────────┐
│  [Icon] AGENT NODE                     ● Running       │
├────────────────────────────────────────────────────────┤
│  Refund Resolution Specialist                          │
│  Model: Claude 3.5 Sonnet | Memory: Session            │
│  Tools: [Stripe Refund] [Zendesk Update]               │
├────────────────────────────────────────────────────────┤
│  Input Port (Target)            Output Port (Source)   │
└────────────────────────────────────────────────────────┘
```

- **Trigger Node**: Blue header. Webhook / Schedule indicator.
- **Agent Node**: Violet header. Shows agent name, bound model, and active tools count.
- **Tool Node**: Emerald header. Shows tool action name and risk badge (`High Risk`).
- **Approval Node**: Amber header. Displays required approver role and timeout countdown badge.
- **Condition Node**: Slate header. Two output ports: `True` (Green) and `False` (Red).

### 4.5 Human-in-the-Loop Approval Center & Review Drawer
- **Approval Card**: Risk level pill badge, target tool name, execution timestamp, requester name, and timeout countdown.
- **Review Drawer (Split-Screen)**:
  - *Left*: Execution Context (Parent workflow, agent thought trace, reason for escalation).
  - *Right*: Proposed Action Payload (Formatted JSON diff view showing target external modifications).
  - *Footer*: Action Buttons: **Approve** (Emerald), **Reject with Reason** (Red), **Request Changes** (Amber).

### 4.6 Execution Timeline & Waterfall Trace Viewer
- Horizontal Gantt/Waterfall chart visualizing parent workflow duration:
  - Each step represented as a color-coded horizontal bar proportional to latency.
  - Expanding an Agent Step reveals internal ReAct reasoning spans, LLM call durations, and tool execution times.
  - Token consumption and dollar cost displayed beside each span.

### 4.7 Knowledge Base & Chunk Inspection UI
- **Collection View**: Document upload drag-and-drop zone with real-time ingestion progress bar (Parsing → Chunking → Embedding → Indexed).
- **Chunk Inspector**: Interactive modal displaying raw document text split into numbered chunks with token count badges and vector similarity scores.

### 4.8 Tool & MCP Server Registry
- Card grid listing registered MCP servers (stdio/HTTP) and built-in tools.
- Each card details: Tool name, transport type, JSON input schema editor, risk classification selector (`Low`, `Medium`, `High`, `Critical`), and test execute button.

---

## 5. RESPONSIVE BREAKPOINTS & ACCESSIBILITY STANDARDS

### Breakpoints
- `sm`: `640px` (Mobile landscape)
- `md`: `768px` (Tablet - Sidebar collapses to icon rail)
- `lg`: `1024px` (Small Desktop - Full navigation enabled)
- `xl`: `1280px` (Desktop - Split-screen studio layouts enabled)
- `2xl`: `1536px` (Wide Desktop - High-density canvas)

### Accessibility Standards
- **Keyboard Traversal**: Full focus-visible rings on interactive controls (`ring-2 ring-brand-primary`).
- **Screen Reader Support**: All icons possess `aria-hidden="true"`; buttons declare explicit `aria-label` tags.
- **Contrast Ratios**: Body text meets a minimum of 4.5:1 contrast against surface backgrounds; large headings meet 3:1.

---

*End of UI/UX Design System Specification*  
*Document Version: 1.0.0 | Status: FINAL & APPROVED*
