YOLOv8Car
專案簡介
YOLOv8Car 是一個使用 YOLOv8 深度學習模型的車輛偵測系統，專為即時偵測車輛距離和追撞風險設計，旨在協助實現車輛前方物體偵測和預警。該專案運行在 Jetson Nano 上，針對嵌入式環境進行了性能優化。

功能特點
即時車輛偵測：利用 YOLOv8 模型進行前方車輛的即時偵測。
距離計算：通過深度學習模型估算與前方車輛的距離。
危險預警：根據車距自動評估追撞風險，並在發生危險時發出警告。
高效運行：針對 Jetson Nano 進行優化，具備低功耗、高效能的優勢。
系統需求
Jetson Nano 開發板
安裝 YOLOv8 所需的依賴庫
Docker（可選，用於環境隔離）
Python 3.8
CUDA 10.2 與 cuDNN 8.2.1
安裝步驟
安裝所需依賴：

bash
複製程式碼
sudo apt update
sudo apt install -y python3-pip
pip install numpy torch torchvision torchaudio opencv-python ultralytics
bash
tensorrt.py有轉換的方法
bash
克隆專案：

bash
複製程式碼
git clone https://github.com/yangting122/yolov8-.git
cd yolov8car
下載權重文件： 將訓練好的 YOLOv8 權重文件（best.pt）放入專案根目錄。

使用說明
啟動偵測程式：

bash
複製程式碼
python main.py
註：若使用 Docker，請先啟動 Docker 容器。
dockerset有相關code

參數設置：

在 config.yaml 中設置偵測參數，包括距離閾值、警告時間等。
輸出結果：

偵測結果會即時顯示在外接螢幕上，並在符合條件時顯示 DANGER 標籤。
貢獻
歡迎對本專案進行改進，並提交 Pull Request。我們會審核所有提交並在合適時合併進主分支。

授權
本專案基於 MIT 許可證發布。詳情請參閱 LICENSE 文件
參考資料https://docs.ultralytics.com/guides/nvidia-jetson/
