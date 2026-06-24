import { useEffect, useRef, useState } from "react";
import medicallogo from "./assets/logo-medical.png"

const API_URL = "http://127.0.0.1:8000";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

export default function App() {
  const [sessionId, setSessionId] = useState(
    localStorage.getItem("session_id") || ""
  );

  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  async function createSession() {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(`${API_URL}/session`, {
        method: "POST",
      });

      if (!response.ok)
        throw new Error("Failed to create session");

      const data = await response.json();

      localStorage.setItem("session_id", data.session_id);
      setSessionId(data.session_id);
      setMessages([]);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function uploadPDF() {
    if (!file) return;

    if (!sessionId) {
      setError("Create a chat first.");
      return;
    }

    try {
      setUploading(true);

      const form = new FormData();
      form.append("file", file);
      form.append("session_id", sessionId);

      const response = await fetch(`${API_URL}/upload/post-file`, {
        method: "POST",
        body: form,
      });

      if (!response.ok)
        throw new Error("Upload failed");

      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: ` ${file.name} uploaded successfully.`,
        },
      ]);

      setFile(null);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  }

  async function sendMessage() {
    if (!input.trim()) return;

    if (!sessionId) {
      setError("Create a chat first.");
      return;
    }

    const question = input;

    setMessages((prev) => [
      ...prev,
      {
        id: crypto.randomUUID(),
        role: "user",
        content: question,
      },
    ]);

    setInput("");
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: question,
          session_id: sessionId,
        }),
      });

      if (!response.ok)
        throw new Error("Failed to get response");

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: data.answer,
        },
      ]);
    } catch (err: any) {
      setError(err.message);

      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: "Something went wrong.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="h-screen bg-zinc-900 text-white flex flex-col">

      {/* Header */}

      <header className="border-b border-zinc-700 p-4 flex justify-between items-center">
        <div>
          <img src={medicallogo} alt="Medical Assistant logo" width={100} height={150} />
          <h1 className="text-2xl font-bold">
            Medical Assistant
          </h1>

          <p className="text-xs text-zinc-400 mt-1">
            Session: {sessionId || "Not created"}
          </p>
        </div>

        <button
          onClick={createSession}
          className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg"
        >
          New Chat
        </button>
      </header>

      {/* Chat */}

      <div className="flex-1 overflow-y-auto p-6 space-y-5">

        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-zinc-400">
            <h2 className="text-4xl font-bold mb-3">
              Medical Assistant
            </h2>

            <p>
              Upload a PDF and ask questions about it.
            </p>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${
              message.role === "user"
                ? "justify-end"
                : "justify-start"
            }`}
          >
            <div
              className={`max-w-3xl px-5 py-3 rounded-2xl whitespace-pre-wrap ${
                message.role === "user"
                  ? "bg-blue-600"
                  : "bg-zinc-800"
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-zinc-800 rounded-2xl px-5 py-3 animate-pulse">
              Thinking...
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {error && (
        <div className="bg-red-600 p-3 text-center">
          {error}
        </div>
      )}

      {/* Upload */}

      <div className="border-t border-zinc-700 p-4 flex gap-3 items-center">

        <input
          type="file"
          accept=".pdf"
          onChange={(e) =>
            setFile(e.target.files?.[0] || null)
          }
          className="text-sm"
        />

        <button
          onClick={uploadPDF}
          disabled={!file || uploading}
          className="bg-green-600 hover:bg-green-700 disabled:bg-gray-600 px-4 py-2 rounded-lg"
        >
          {uploading ? "Uploading..." : "Upload"}
        </button>

        {file && (
          <span className="text-sm text-zinc-300">
            {file.name}
          </span>
        )}
      </div>

      {/* Input */}

      <div className="border-t border-zinc-700 p-4 flex gap-3">

        <input
          className="flex-1 bg-zinc-800 rounded-xl px-4 py-3 outline-none"
          placeholder="Ask something about your PDF..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) =>
            e.key === "Enter" && !loading && sendMessage()
          }
        />

        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 px-6 rounded-xl"
        >
          Send
        </button>
      </div>
    </div>
  );
}