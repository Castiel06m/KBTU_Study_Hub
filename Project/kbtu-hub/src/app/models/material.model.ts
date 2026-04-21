export interface Material {
  id: number;
  title: string;
  description: string;
  fileUrl: string; 
  type: 'Lecture' | 'Lab' | 'Practice' | 'Other';
  courseId: number;
  uploadedBy: number; 
  createdAt: Date;
}