# HealthCare App

A comprehensive healthcare application built with React, TypeScript, and Tailwind CSS. This app provides AI-powered symptom checking, doctor discovery, health history tracking, and an intelligent health assistant.

## 🏥 Features

### 1. AI Assistant

- 24/7 available health AI assistant
- Chat interface for health questions
- Emergency guidance and recommendations
- General health information and tips

### 2. Symptom Checker

- Interactive selection from  symptoms across 8 categories
- AI-powered disease prediction and analysis
- Medical triage with urgency levels

### 3. Health History Tracking

- Complete consultation history
- Search and filter capabilities
- Follow-up tracking
- Export functionality
- Statistical insights

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- npm, yarn, or pnpm

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd healthcare-app
```

2. Install dependencies:

```bash
npm install
# or
yarn install
# or
pnpm install
```

3. Start the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

4. Open your browser and visit `http://localhost:8080`

## 🏗️ Technical Architecture

### Frontend Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **React Router** - Client-side routing
- **Vite** - Build tool and dev server

### UI Components

- **shadcn/ui** - Component library built on Radix UI
- **Lucide React** - Icon library
- **Framer Motion** - Animations
- **Date-fns** - Date utilities

### State Management

- **React Context** - Global health app state
- **Firebase Storage** - Data persistence
- **TanStack Query** - Server state management

### Key Features

- **Responsive Design** - Mobile-first approach
- **Accessibility** - ARIA compliant components
- **Type Safety** - Comprehensive TypeScript coverage
- **Performance** - Optimized bundles and lazy loading

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── ui/             # shadcn/ui components
│   ├── Navigation.tsx  # App navigation
│   ├── SymptomSelector.tsx
│   ├── DiseaseCard.tsx
│   ├── DoctorCard.tsx
│   ├── TriageDisplay.tsx
│   ├── HistoryItem.tsx
│   ├── ChatInterface.tsx
│   └── LocationMap.tsx
├── pages/              # Page components
│   ├── Dashboard.tsx   # Main dashboard
│   ├── SymptomChecker.tsx
│   ├── Results.tsx
│   ├── DoctorLocator.tsx
│   ├── History.tsx
│   ├── AIAssistant.tsx
│   └── NotFound.tsx
├── context/            # React contexts
│   └── HealthContext.tsx
├── hooks/              # Custom React hooks
│   ├── useHealthHistory.ts
│   └── useGeolocation.ts
├── data/               # Static data and databases
│   ├── symptoms.ts     # 60+ symptoms database
│   ├── diseases.ts     # Disease conditions database
│   └── doctors.ts      # Healthcare providers database
├── lib/                # Utility functions
│   ├── utils.ts        # General utilities
│   └── healthUtils.ts  # Health-specific utilities
├── types/              # TypeScript definitions
│   └── health.ts       # Health-related interfaces
└── App.tsx             # Main app component
```

## 🔧 Key Components

### HealthContext

Global state management for:

- Selected symptoms
- Current predictions
- Health history
- Chat messages
- User profile
- Loading states

### Symptom Checker Flow

1. **SymptomSelector** - Interactive symptom selection
2. **AI Analysis** - Process symptoms and generate predictions
3. **Results** - Display predictions, triage, and recommendations

### Data Models

- **Symptom** - Individual symptoms with categories and severity
- **Disease** - Medical conditions with symptom mappings
- **PredictionResult** - AI analysis results with triage
- **HealthHistory** - Historical consultation records

## 🎨 Design System

### Color Scheme

- **Primary** - Blue tones for trust and reliability
- **Secondary** - Green for health and wellness
- **Alert Colors** - Red (emergency), Orange (high), Yellow (medium), Green (low)

### Typography

- **Font Family** - System fonts for optimal readability
- **Scale** - Consistent sizing from text-xs to text-4xl
- **Weight** - Regular, medium, semibold, and bold variants

### Components

- **Cards** - Primary container format
- **Badges** - Status indicators and tags
- **Buttons** - Clear call-to-action hierarchy
- **Forms** - Accessible input components

## 🔐 Data & Privacy

### Firebase Storage

- Health history stored locally
- User preferences and settings
- Chat message history
- No sensitive data transmitted

### Mock Data

- Sample symptoms, diseases, and doctors
- Realistic AI responses for demonstration
- No real medical advice provided

### Disclaimers

- Educational purposes only
- Not a substitute for professional medical advice
- Emergency situations require immediate medical attention

## 🚀 Deployment

### Build for Production

```bash
npm run build
# or
yarn build
# or
pnpm build
```

### Deploy to Vercel

```bash
npm i -g vercel
vercel
```

### Deploy to Netlify

```bash
npm run build
# Upload the `dist` folder to Netlify
```

## 🧪 Testing

### Run Tests

```bash
npm test
# or
yarn test
# or
pnpm test
```

### Type Checking

```bash
npm run typecheck
# or
yarn typecheck
# or
pnpm typecheck
```

## 📋 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run test` - Run tests
- `npm run typecheck` - TypeScript checking
- `npm run format.fix` - Format code with Prettier

## 🔮 Future Enhancements

### Version 2.0 Features

- **Interactive Maps** - Google Maps integration for doctor locations
- **Appointment Booking** - Real booking system integration
- **Telemedicine** - Video consultation capabilities
- **Wearable Integration** - Health device data import
- **Advanced AI** - More sophisticated symptom analysis
- **Multi-language Support** - Internationalization
- **Offline Mode** - Progressive Web App features

### Integrations

- **Electronic Health Records (EHR)** - Medical record integration
- **Insurance Verification** - Real-time insurance checking
- **Pharmacy Integration** - Prescription management
- **Lab Results** - Test result integration

## ⚠️ Important Disclaimers

1. **Medical Advice**: This application provides general health information and should not replace professional medical advice, diagnosis, or treatment.

2. **Emergency Situations**: In case of medical emergencies, call 911 or go to the nearest emergency room immediately.

3. **Accuracy**: While the app uses evidence-based information, it cannot guarantee 100% accuracy in predictions or recommendations.

4. **Professional Consultation**: Always consult with qualified healthcare providers for medical concerns and treatment decisions.

## 📄 License

This project is built for educational and demonstration purposes. All medical information is for general guidance only.

## 🤝 Contributing

Contributions are welcome! Please ensure any medical information added is from reputable sources and includes appropriate disclaimers.

---

**Remember: This app is for educational purposes only. Always seek professional medical advice for health concerns.**
