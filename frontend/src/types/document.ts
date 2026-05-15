export interface DocumentItem {
  id: number;
  filename: string;
  file_path: string;
  upload_status: string;
  owner_id: number;
  pages: number | null;
  title: string | null;
  author: string | null;
  file_size: number;
  created_at: string;
}