import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

const client = axios.create({ baseURL: BASE_URL, timeout: 15000 });

export async function fetchSkillsTaxonomy() {
  const { data } = await client.get("/skills");
  return data.skills;
}

export async function fetchInterestTags() {
  const { data } = await client.get("/interests");
  return data.interests;
}

export async function getRecommendations(profile) {
  const { data } = await client.post("/recommend", profile);
  return data;
}

export default client;
