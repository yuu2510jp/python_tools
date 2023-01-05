try:
    import pandas as pd
    import pathlib
except:
    import pip, site, importlib
    pip.main(['install', 'pandas'])
    pip.main(['install', 'pathlib'])
    importlib.reload(site)
    import pandas as pd
    import pathlib


class DirectoryService:
    OUTPUT_DIR_NAME = 'output'
    
    def __init__(self, sort_target_dir_path, output_dir_path):
        self.sort_target_dir = pathlib.Path(sort_target_dir_path)
        self.output_dir = pathlib.Path(output_dir_path) / self.OUTPUT_DIR_NAME
        self.create_directory(self.output_dir)
        
    def get_sort_target_files(self):
        '''get file names in direcoty path
        '''
        root = pathlib.Path(self.sort_target_dir)
        return root.iterdir()
    
    def create_directory(self, dir) -> None:
        '''create output direcoty if it not exists
        '''
        if not dir.exists():
            dir.mkdir()
            
    def get_output_directory_path(self, cls: str):
        output_dir = self.output_dir / cls
        self.create_directory(output_dir)
        return output_dir.resolve()


class MappingService:
    
    def __init__(self, mapping_csv):
        self.mapping_df = pd.read_csv(mapping_csv)
        self.files = list(self.mapping_df["file_name"])
        
    def get_class(self, file_name):
        if file_name in self.files:
            return list(self.mapping_df.loc[self.mapping_df['file_name']==file_name, 'class'])[0]
        else:
            return 'no_class'
        
import shutil

def main(sort_target_dir_path: str,
         mapping_csv_path: str) -> None:
    '''Sort files along with definition dataframe
    '''
    dir_service = DirectoryService(sort_target_dir_path, '.')
    mapping = MappingService(mapping_csv_path)
    
    for file in dir_service.get_sort_target_files():
        cls = mapping.get_class(file.name)
        output_directory_path = dir_service.get_output_directory_path(cls)
        shutil.copy(file.resolve(), output_directory_path)
        


if __name__ == '__main__':
    import sys
    args = sys.argv
    
    try:
        if not 1 < len(args) < 4:
            raise Exception('引数の数が不正')
        
        sort_target_dir_path = args[1]
        mapping_csv_path = args[2] if len(args)==3 else './mapping.csv'
        main(sort_target_dir_path, mapping_csv_path)
        
    except Exception as e:
        print(e)
        print('第1引数->分類したいファイルが入っているディレクトリのパス')
        print('第2引数->分類のマッピング用csvのパス')