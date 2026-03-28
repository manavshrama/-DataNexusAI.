const API_BASE_URL = "http://localhost:8000";

export async function fetchInsights() {
  const res = await fetch(`${API_BASE_URL}/insights`);
  if (!res.ok) throw new Error("Failed to fetch insights");
  return res.json();
}

export async function uploadDataset(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  
  const res = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error("Failed to upload dataset");
  return res.json();
}

export async function getStats(sessionId: str) {
  const res = await fetch(`${API_BASE_URL}/stats/${sessionId}`);
  if (!res.ok) throw new Error("Failed to fetch stats");
  return res.json();
}
