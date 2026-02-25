import { useState } from "react";
import { KanbanBoard } from "../components/board/KanbanBoard";
import { useAuth } from "../hooks/useAuth";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import { Search } from "lucide-react";

export function Board() {
  const { logout, user } = useAuth();
  const [search, setSearch] = useState("");
  const [priority, setPriority] = useState<string>("");

  // URL sync would usually happen via react-router useSearchParams
  // Doing it in component state for simplicity per Weekend 2 specs.

  return (
    <div className="flex h-screen flex-col bg-gray-50">
      <header className="flex h-16 shrink-0 items-center justify-between border-b border-gray-200 bg-white px-6">
        <h1 className="text-xl font-bold tracking-tight text-indigo-600">
          HuntBoard
        </h1>

        <div className="flex flex-1 items-center justify-center px-8">
          <div className="flex w-full max-w-2xl items-center gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                id="search"
                type="text"
                placeholder="Search company or role..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-9"
              />
            </div>
            <select
              value={priority}
              onChange={(e) => setPriority(e.target.value)}
              className="h-10 rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:border-transparent focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="">All Priorities</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <span className="text-sm font-medium text-gray-700">
            {user?.full_name}
          </span>
          <Button variant="ghost" size="sm" onClick={logout}>
            Sign out
          </Button>
        </div>
      </header>

      <main className="flex-1 overflow-hidden">
        <KanbanBoard filters={{ search, priority }} />
      </main>
    </div>
  );
}
