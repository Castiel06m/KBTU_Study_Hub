export interface Category {
  id: number;
  name: string;
}

export interface Course {
  id: number;
  title: string;
  description: string;
  category: number;
  category_name?: string;
  author_name?: string;
  author: number;
  lessons: Lesson[];
  comments: Comment[]; 
  is_enrolled: boolean;
}

export interface Lesson {
  id: number;
  title: string;
  content: string;
  video_url?: string; 
  file?: string;
}

export interface LessonCreate {
  title: string;
  content: string;
  course: number;
  order?: number;
  video_url?: string;
  file?: File | null;
}

export interface Comment {
  id: number;
  user_name: string;
  text: string;
  created_at: string;
}

export interface Guild {
  id: number;
  name: string;
  description: string;
  leader_name: string;  
  members_count: number;
}