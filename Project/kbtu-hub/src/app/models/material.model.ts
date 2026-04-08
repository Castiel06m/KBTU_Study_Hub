export interface Material {
  id: number;
  title: string;
  description: string;
  fileUrl: string; // Ссылка на скачивание
  type: 'Lecture' | 'Lab' | 'Practice' | 'Other';
  courseId: number;
  uploadedBy: number; // ID пользователя
  createdAt: Date;
}