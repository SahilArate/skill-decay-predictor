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

  useEffect(() => {
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
  }, []);

  if (loading) return <main className="p-8">Loading skills...</main>;
  if (error) return <main className="p-8 text-red-500">{error}</main>;

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">Your Skills</h1>
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