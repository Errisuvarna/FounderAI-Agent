import axiosClient from './axiosClient'

export async function registerUser({ name, email, password }) {
  const { data } = await axiosClient.post('/register', { name, email, password })
  return data
}

export async function loginUser({ email, password }) {
  const { data } = await axiosClient.post('/login', { email, password })
  return data
}

export async function fetchProfile() {
  const { data } = await axiosClient.get('/profile')
  return data
}

export async function generateBlueprint({ idea_title, idea_description, industry, target_market }) {
  const { data } = await axiosClient.post('/generate', {
    idea_title,
    idea_description,
    industry,
    target_market,
  })
  return data
}
