import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

// Interfaces para o TypeScript (devem bater com seus Schemas do Pydantic)
export interface Produto {
  id: number;
  nome: string;
  preco: number;
  quantidade_estoque: number;
}

export type ProdutoInput = Omit<Produto, 'id'>;

export const adminService = {
  // Listar todos
  listarProdutos: () => api.get<Produto[]>('/admin/produtos/'),
  
  // Criar novo
  criarProduto: (dados: ProdutoInput) => api.post<Produto>('/admin/produtos/', dados),
  
  // Editar
  editarProduto: (id: number, dados: Partial<ProdutoInput>) => 
    api.put<Produto>(`/admin/produtos/${id}`, dados),
  
  // Deletar
  excluirProduto: (id: number) => api.delete(`/admin/produtos/${id}`),
};