"""Restaura em uma pasta nova, recusando sobrescrita e caminhos externos."""
import argparse
import json
from pathlib import Path,PurePosixPath
import sqlite3
import zipfile

def restore(backup,destination):
    destination=Path(destination).resolve()
    if destination.exists() and any(destination.iterdir()):
        raise ValueError('Escolha uma pasta nova ou vazia. O acervo existente não será substituído.')
    with zipfile.ZipFile(backup) as archive:
        if json.loads(archive.read('manifest.json')).get('format')!='observatorio-backup-v1':
            raise ValueError('Formato de backup não reconhecido.')
        members=archive.infolist()
        if sum(m.file_size for m in members)>10_000_000_000:
            raise ValueError('Backup excede limite de restauração de 10 GB.')
        for item in members:
            name=PurePosixPath(item.filename.replace('\\','/'))
            if name.is_absolute() or '..' in name.parts or ':' in item.filename:
                raise ValueError('Backup contém caminho inválido.')
            if item.filename not in {'manifest.json','observatorio.sqlite3'} and name.parts[0] not in {'audio','documents','images'}:
                raise ValueError('Backup contém um arquivo não permitido.')
            if (item.external_attr>>16)&0o170000==0o120000:
                raise ValueError('Links simbólicos não são aceitos no backup.')
        destination.mkdir(parents=True,exist_ok=True)
        for item in members:
            target=(destination/item.filename).resolve()
            if not target.is_relative_to(destination):
                raise ValueError('Caminho fora do destino.')
            if item.is_dir():
                target.mkdir(parents=True,exist_ok=True)
            else:
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(archive.read(item))
    connection=sqlite3.connect(destination/'observatorio.sqlite3')
    try:
        if connection.execute('PRAGMA integrity_check').fetchone()[0]!='ok':
            raise ValueError('O banco restaurado não passou na verificação de integridade.')
    finally:
        connection.close()
    return destination

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('backup')
    parser.add_argument('destination')
    args=parser.parse_args()
    try:
        target=restore(args.backup,args.destination)
        print(f'Backup restaurado em {target}. Configure OBS_DATA_DIR para usar essa pasta. A chave da API deve ser cadastrada novamente.')
    except (ValueError,KeyError,zipfile.BadZipFile) as error:
        raise SystemExit(str(error))
