"use client";

import { useEffect, useState } from "react";

type Skill = {
  id: string;
  name: string;
  category: string;
  last_practiced_at: string;
  stability: number;
};

export default function Home() {
  const [skills, setSkills] = useState<Skill[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [name, setName] = useState("");
  const [category, setCategory] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const fetchSkills = () => {
    setLoading(true);
    fetch("http://127.0.0.1:8000/skills")
      .then((res) => res.json())
      .then((data) => {
        setSkills(data);
        setLoading(false);
      })
      .catch(() => {
        setError("Could not load skills. Is the backend running?");
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchSkills();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;

    setSubmitting(true);
    try {
      await fetch("http://127.0.0.1:8000/skills", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, category: category || null }),
      });
      setName("");
      setCategory("");
      fetchSkills();
    } catch {
      setError("Could not create skill.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <main className="p-8">Loading skills...</main>;
  if (error) return <main className="p-8 text-red-500">{error}</main>;

  return (
    <main className="p-8 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Your Skills</h1>

      <form onSubmit={handleSubmit} className="mb-6 flex gap-2">
        <input
          type="text"
          placeholder="Skill name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="border p-2 rounded flex-1"
        />
        <input
          type="text"
          placeholder="Category (optional)"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="border p-2 rounded flex-1"
        />
        <button
          type="submit"
          disabled={submitting}
          className="bg-black text-white px-4 py-2 rounded disabled:opacity-50"
        >
          {submitting ? "Adding..." : "Add"}
        </button>
      </form>

      <ul className="space-y-2">
        {skills.map((skill) => (
          <li key={skill.id} className="border p-3 rounded">
            <p className="font-semibold">{skill.name}</p>
            <p className="text-sm text-gray-500">{skill.category}</p>
          </li>
        ))}
      </ul>
    </main>
  );
}