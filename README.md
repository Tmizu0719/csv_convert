# csv_convert
 this program converts csv file to matrix 

このプログラムはヘッダーを持つcsvファイルを，ヘッダーとデータにそれぞれlistとnumpyarrayの形式に変換し，のちのデータ処理を容易く行うためのプログラムである．
欠損データはnumpy.nanで穴埋めされる．
また簡易的な機能として，欠損データ削除と欠損データの置換を行えるようにした．
添付している テストデータは３，６行目に欠損データを与えている．

～～使い方～～
CC = CsvConvert()                                         ＃クラスを作成
header, data = CC.convert_np("csv_matrix/test_data.csv")  ＃パスを引数として入力，ヘッダーとデータの変数名を指定する．

上記の例だとheaderにはヘッダーのlist, dataにはヘッダー以下の数値データのnumpy.arrayが格納される．変数名を指定しない場合，タプルの中にheader, dataが格納される．

欠損データの削除
欠損データを含む行を削除する．このとき削除した行数（ヘッダーを除き，1から始まる．）がprintされる．
欠損データがない場合，元の行列が返る．
CC.delete_nanrow(data)  ＃引数にnumpy.arrayを入力

欠損データの置換
欠損データを検索して2引数に入力した数値で置換する．
CC.replace_nan(data, 0)  ＃１引数はnumpy.array, ２引数は置換したい数値（この例では０）

※他のプログラムにインポートして使用したい場合は，他のプログラムと同じディレクトリ内にこのプログラムを置き，他のプログラムで
from csv_convert import CsvConvert
でインポートして使用する．
