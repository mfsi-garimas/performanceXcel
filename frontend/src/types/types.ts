export interface Response {
  status: string;
  data: Record<string, any>;
}

export interface Rubric {
  id: number;
  rubric_title: string;
  rubric_path: string;
  created_date: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  role: string;
  created_date: string;
}
