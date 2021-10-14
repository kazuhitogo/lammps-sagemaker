# lampps-sagemaker

##  [LAMMPS](https://www.lammps.org/) を Amazon SageMaker Processing でサンプル


SageMaker Processing (with BYOC) で LAMMPS を用いたポリエチレン分子シミュレーションを動かす。細かい情報は下記を参照。

  * [LAMMPSのマニュアル](https://docs.lammps.org/Manual.html)
  * [ポリエチレン分子をシミュレーション](https://winmostar.com/jp/tutorials/LAMMPS_tutorial_8%28Polymer_Elongation%29.pdf)
  * [SageMaker SDK doc](https://sagemaker.readthedocs.io/en/stable/amazon_sagemaker_processing.html)
  * [SageMaker Processing 開発者ガイド](https://docs.aws.amazon.com/sagemaker/latest/dg/processing-job.html)
  
## 前提

* Amazon SageMaker Notebook(≠Studio)を前提  
  docker コマンドを使うため(Studioを使う場合は sm-docker コマンドに修正の必要あり)
* GPUインスタンス(ml.g4dn.xlargeで動作確認)を前提
  ビルドしたコンテナをローカル(SageMaker Notebook内)でテスト実行するのにあたり、GPU で動かす必要があるため
* EBS は 30GB以上 アタッチ
  