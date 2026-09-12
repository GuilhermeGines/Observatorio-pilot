// All documents and API responses in this test file are explicitly synthetic fixtures.
import React from 'react';
import {afterEach,beforeEach,describe,expect,it,vi} from 'vitest';
import {cleanup,fireEvent,render,screen,waitFor} from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import {App} from './main';
import {api,dayOffset} from './api';
vi.mock('./api',async(importOriginal)=>{const actual=await importOriginal<typeof import('./api')>();return {...actual,initialize:vi.fn(async()=>({token:'SYNTHETIC-TEST-TOKEN'})),api:vi.fn()}});
const mocked=vi.mocked(api);
const settings={provider:'openai',model:'synthetic-model',allow_ai:false,key_configured:false,disabled_sources:[],usage:[],counts:{documents:0,revisions:0,analyses:0,audio:0},max_documents:12,max_chars_per_document:6000,max_output_tokens:6000,articles_per_source:3};
const fixture={id:'synthetic-query',status:'pronta',saved_at:null,title:'FIXTURE SINTÉTICA',filters:{countries:['BR','US'],topics:[],keyword:'Samsung',start:'2026-09-07',end:'2026-09-07',mode:'archive'},analyses:[],result:{documents:[],coverage:[],undated_excluded:0,origin_groups:[],related_pairs:[],limitations:['FIXTURE SINTÉTICA'],total_matches:0,truncated:false}};
beforeEach(()=>{mocked.mockReset();mocked.mockImplementation(async(path,method,body)=>{if(path==='/settings')return settings;if(path==='/providers/usage')return {providers:[]};if(path==='/sources')return [];if(path==='/queries')return {id:'synthetic-query',status:'coletando'};if(path==='/queries/synthetic-query')return fixture;if(path==='/queries/synthetic-query/save')return {...fixture,saved_at:'2026-09-07T12:00:00Z'};if(path.startsWith('/history'))return [];return {}})});
afterEach(cleanup);
it('ativa a busca ampliada nas configurações sem iniciar uma consulta',async()=>{
 render(<App/>);
 await screen.findByLabelText('Palavra-chave');
 fireEvent.click(screen.getByRole('button',{name:'Configurações'}));
 fireEvent.click(screen.getByRole('checkbox',{name:'Busca ampliada com Gemini'}));
 fireEvent.click(screen.getByRole('button',{name:/Salvar esta IA/}));
 await waitFor(()=>expect(mocked).toHaveBeenCalledWith('/settings','PUT',expect.objectContaining({gemini_search_enabled:true})));
 expect(mocked.mock.calls.some(call=>call[0]==='/queries')).toBe(false);
});
it('atalho Semana seleciona os últimos sete dias incluindo hoje',async()=>{
 render(<App/>);
 await screen.findByLabelText('Palavra-chave');
 fireEvent.click(screen.getByRole('button',{name:'Semana'}));
 expect(screen.getByLabelText('Tipo de período')).toHaveValue('range');
 const inicio=(screen.getByLabelText('Data inicial') as HTMLInputElement).value;
 const fim=(screen.getByLabelText('Data final') as HTMLInputElement).value;
 const dataInicio=new Date(`${inicio}T12:00:00`);
 const dataFim=new Date(`${fim}T12:00:00`);
 expect((dataFim.getTime()-dataInicio.getTime())/86400000).toBe(6);
 expect(fim).toBe(dayOffset(0));
});
describe('Fluxos essenciais sem gastar API',()=>{
 it('renderiza globo real e mantém países ao digitar Samsung',async()=>{render(<App/>);await screen.findByRole('heading',{name:/Explore os fatos/});expect(document.querySelectorAll('svg.globe path[data-country]').length).toBeGreaterThan(150);fireEvent.change(screen.getByLabelText('Palavra-chave'),{target:{value:'Samsung'}});expect(screen.getByRole('button',{name:/BR Brasil/})).toHaveAttribute('aria-pressed','true');expect(screen.getByRole('button',{name:/CN China/})).toHaveAttribute('aria-pressed','false');fireEvent.click(screen.getByRole('button',{name:/CN China/}));expect(screen.getByRole('button',{name:/CN China/})).toHaveAttribute('aria-pressed','true')});
 it('atalho ontem usa data única e consulta não salva automaticamente',async()=>{render(<App/>);await screen.findByLabelText('Palavra-chave');fireEvent.click(screen.getByRole('button',{name:'Ontem'}));expect(screen.getByLabelText('Tipo de período')).toHaveValue('day');expect(screen.queryByLabelText('Data final')).toBeNull();fireEvent.change(screen.getByLabelText('Palavra-chave'),{target:{value:'Samsung'}});fireEvent.click(screen.getByRole('button',{name:'Buscar no acervo'}));await waitFor(()=>expect(mocked).toHaveBeenCalledWith('/queries','POST',expect.objectContaining({countries:['BR','US'],keyword:'Samsung',mode:'archive'})));const body=mocked.mock.calls.find(c=>c[0]==='/queries')![2] as any;expect(body.start).toBe(body.end);await screen.findByRole('button',{name:'Salvar no histórico'},{timeout:4000});expect(mocked.mock.calls.some(c=>c[0].endsWith('/save'))).toBe(false);fireEvent.click(screen.getByRole('button',{name:'Salvar no histórico'}));await screen.findByRole('button',{name:'Salva no histórico'});expect(mocked.mock.calls.some(c=>c[0].endsWith('/analyze'))).toBe(false)});
 it('navega entre as três páginas e não inventa análise sem chave',async()=>{render(<App/>);await screen.findByLabelText('Palavra-chave');fireEvent.click(screen.getByRole('button',{name:'Histórico'}));await screen.findByRole('heading',{name:'Volte às suas perguntas.'});fireEvent.click(screen.getByRole('button',{name:'Configurações'}));await screen.findByText('Sem chave');expect(screen.getByLabelText('Chave da API OpenAI')).toHaveAttribute('type','password');fireEvent.click(screen.getByRole('button',{name:'Explorar'}));await screen.findByRole('heading',{name:/Explore os fatos/});expect(mocked.mock.calls.some(c=>c[0].endsWith('/analyze'))).toBe(false)});
});
