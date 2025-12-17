import { BrowserRouter, Routes, Route } from "react-router-dom"
import { Layout } from "@/components/layout"
import {
  DashboardPage,
  TestCasesPage,
  PyTestPage,
  AnalyzePage,
  GitHubPage,
  SettingsPage,
} from "@/pages"

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/testcases" element={<TestCasesPage />} />
          <Route path="/pytest" element={<PyTestPage />} />
          <Route path="/analyze" element={<AnalyzePage />} />
          <Route path="/github" element={<GitHubPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}

export default App
