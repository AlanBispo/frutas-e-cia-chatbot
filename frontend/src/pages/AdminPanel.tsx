import React, { useEffect, useState, useMemo } from 'react';
import { adminService, type Produto, type ProdutoInput } from '../services/adminService';
import { 
  Plus, Search, Edit2, Trash2, Package, 
  DollarSign, BarChart3, X, Save, Loader2 
} from 'lucide-react';

const AdminPanel: React.FC = () => {
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('');
  const [form, setForm] = useState<ProdutoInput>({ nome: '', preco: 0, quantidade_estoque: 0 });
  const [editId, setEditId] = useState<number | null>(null);

  const carregarProdutos = async () => {
    setLoading(true);
    try {
      const response = await adminService.listarProdutos();
      setProdutos(response.data);
    } catch (error) {
      console.error("Erro ao carregar estoque");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { carregarProdutos(); }, []);

  // Filtro dinâmico
  const produtosFiltrados = useMemo(() => {
    return produtos.filter(p => p.nome.toLowerCase().includes(filter.toLowerCase()));
  }, [produtos, filter]);

  // Estatísticas rápidas
  const totalItens = produtos.reduce((acc, p) => acc + p.quantidade_estoque, 0);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editId) {
        await adminService.editarProduto(editId, form);
      } else {
        await adminService.criarProduto(form);
      }
      setForm({ nome: '', preco: 0, quantidade_estoque: 0 });
      setEditId(null);
      carregarProdutos();
    } catch (error) {
      alert("Erro ao salvar produto!");
    }
  };

  const handleExcluir = async (id: number) => {
    if (confirm("Deseja mesmo remover este item?")) {
      await adminService.excluirProduto(id);
      carregarProdutos();
    }
  };

  if (loading && produtos.length === 0) {
    return (
      <div className="flex h-screen w-full items-center justify-center bg-slate-50">
        <Loader2 className="h-10 w-10 animate-spin text-emerald-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 p-4 md:p-8 font-sans text-slate-900">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight text-slate-800">
              Estoque <span className="text-emerald-600">Frutas & Cia</span>
            </h1>
            <p className="text-slate-500">Gerencie seus produtos e níveis de estoque em tempo real.</p>
          </div>
          <div className="flex items-center gap-2 text-sm font-medium text-slate-500 bg-white p-2 rounded-lg shadow-sm border border-slate-200">
             <span className="flex items-center gap-1 px-2 border-r border-slate-200">
                <Package size={16} className="text-emerald-500" /> {produtos.length} Tipos
             </span>
             <span className="flex items-center gap-1 px-2">
                <BarChart3 size={16} className="text-blue-500" /> {totalItens} Unidades
             </span>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Formulário lateral (Card) */}
          <div className="lg:col-span-4">
            <div className="bg-white p-6 rounded-2xl shadow-md border border-slate-200 sticky top-8">
              <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                {editId ? <Edit2 size={20} className="text-blue-500" /> : <Plus size={20} className="text-emerald-500" />}
                {editId ? 'Editar Produto' : 'Novo Produto'}
              </h2>
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold mb-1 text-slate-700">Nome da Fruta</label>
                  <input 
                    value={form.nome} 
                    onChange={e => setForm({...form, nome: e.target.value})} 
                    className="w-full px-4 py-2 rounded-xl border border-slate-200 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 outline-none transition-all"
                    placeholder="Ex: Manga Palmer"
                    required 
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold mb-1 text-slate-700">Preço (R$)</label>
                    <input 
                      type="number" step="0.01" 
                      value={form.preco} 
                      onChange={e => setForm({...form, preco: Number(e.target.value)})} 
                      className="w-full px-4 py-2 rounded-xl border border-slate-200 focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                      required 
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold mb-1 text-slate-700">quantidade_estoque</label>
                    <input 
                      type="number" 
                      value={form.quantidade_estoque} 
                      onChange={e => setForm({...form, quantidade_estoque: Number(e.target.value)})} 
                      className="w-full px-4 py-2 rounded-xl border border-slate-200 focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                      required 
                    />
                  </div>
                </div>

                <div className="flex gap-2 pt-2">
                  <button 
                    type="submit"
                    className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2.5 rounded-xl transition-colors flex items-center justify-center gap-2 shadow-lg shadow-emerald-200"
                  >
                    <Save size={18} />
                    {editId ? 'Atualizar' : 'Adicionar'}
                  </button>
                  {editId && (
                    <button 
                      type="button"
                      onClick={() => {setEditId(null); setForm({nome:'', preco:0, quantidade_estoque:0})}}
                      className="bg-slate-100 hover:bg-slate-200 text-slate-600 p-2.5 rounded-xl transition-colors"
                    >
                      <X size={20} />
                    </button>
                  )}
                </div>
              </form>
            </div>
          </div>

          {/* Listagem/Tabela */}
          <div className="lg:col-span-8 space-y-4">
            {/* Barra de Busca */}
            <div className="relative group">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-emerald-500 transition-colors" size={20} />
              <input 
                type="text"
                placeholder="Buscar por nome da fruta..."
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="w-full pl-12 pr-4 py-3 rounded-2xl border border-slate-200 bg-white shadow-sm focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
              />
            </div>

            {/* Tabela Responsiva */}
            <div className="bg-white rounded-2xl shadow-md border border-slate-200 overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="bg-slate-50 border-b border-slate-100">
                      <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-slate-500">Produto</th>
                      <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-slate-500 text-center">Estoque</th>
                      <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-slate-500">Preço Un.</th>
                      <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-slate-500 text-right">Ações</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {produtosFiltrados.map(p => (
                      <tr key={p.id} className="hover:bg-slate-50/80 transition-colors group">
                        <td className="px-6 py-4">
                          <span className="font-semibold text-slate-700">{p.nome}</span>
                        </td>
                        <td className="px-6 py-4 text-center">
                          <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                            p.quantidade_estoque < 10 ? 'bg-orange-100 text-orange-600' : 'bg-blue-100 text-blue-600'
                          }`}>
                            {p.quantidade_estoque} un
                          </span>
                        </td>
                        <td className="px-6 py-4 font-medium text-slate-600">
                          R$ {p.preco.toFixed(2)}
                        </td>
                        <td className="px-6 py-4 text-right">
                          <div className="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                            <button 
                              onClick={() => { setForm(p); setEditId(p.id); window.scrollTo({top: 0, behavior: 'smooth'}); }}
                              className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                              title="Editar"
                            >
                              <Edit2 size={18} />
                            </button>
                            <button 
                              onClick={() => handleExcluir(p.id)}
                              className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                              title="Excluir"
                            >
                              <Trash2 size={18} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                    {produtosFiltrados.length === 0 && (
                      <tr>
                        <td colSpan={4} className="px-6 py-12 text-center text-slate-400">
                          Nenhum produto encontrado.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};

export default AdminPanel;