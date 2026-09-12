import React from 'react';
import {afterEach,expect,it,vi} from 'vitest';
import {cleanup,fireEvent,render,screen} from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import {CountrySummaries} from './main';
import {Doc} from './api';

afterEach(cleanup);
it('alterna narrativas por país e preserva referências recolhidas sem duplicar fontes',()=>{
 const documents=[{revision_id:1,country:'BR',source_name:'Fonte fictícia',title:'Notícia fictícia',text:'Texto de teste',published_at:null,access:'texto_extraido',genre:''}] as Doc[];
 const analysis={result:{summaries:[{country:'BR',text:'Narrativa brasileira.',evidence:[{revision_id:1,quote:'Texto de teste'}]},{country:'BR',text:'Segundo parágrafo.',evidence:[{revision_id:1,quote:'Texto de teste'}]},{country:'US',text:'English narrative.',evidence:[]}]}};
 const open=vi.fn();
 render(<CountrySummaries codes={['BR','US','CN']} analysis={analysis} documents={documents} open={open}/>);
 expect(screen.getByText('Narrativa brasileira.')).toBeVisible();
 expect(screen.getByText('English narrative.')).not.toBeVisible();
 const refs=screen.getByText('Consultar referências · 1').closest('details')!;
 expect(refs).not.toHaveAttribute('open');
 fireEvent.click(screen.getByRole('tab',{name:/Estados Unidos/}));
 expect(screen.getByText('English narrative.')).toBeVisible();
 expect(screen.getByText('Narrativa brasileira.')).not.toBeVisible();
 fireEvent.keyDown(screen.getByRole('tab',{name:/Estados Unidos/}),{key:'ArrowRight'});
 expect(screen.getByRole('tab',{name:/China/})).toHaveFocus();
 expect(screen.getByText('Nenhuma notícia encontrada para este país no recorte atual.')).toBeVisible();
 fireEvent.click(screen.getByRole('tab',{name:/Brasil/}));
 refs.open=true;
 fireEvent.click(screen.getByRole('button',{name:/Fonte fictícia · Notícia fictícia/}));
 expect(open).toHaveBeenCalledWith(documents[0]);
});
