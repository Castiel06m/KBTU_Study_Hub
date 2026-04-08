export interface Course {
  id: number;
  title: string;
  code: string; // Например CSCI 1202 
  description?: string;
  // Место для логотипа пока
  logoUrl?: string; 
}