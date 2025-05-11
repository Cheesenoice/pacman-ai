# Pacman AI

Dự án Python triển khai các thuật toán tìm kiếm trí tuệ nhân tạo trong môi trường Pacman của UC Berkeley (Pac-Man Projects). Giúp Pacman tìm đường đến thức ăn, ăn capsule trước khi thu thập hết thức ăn, sử dụng tìm kiếm không thông tin và có thông tin.

<p align="center">
<img src="https://github.com/rojinakashefi/Pacman-AI/blob/main/interactive.gif" width="540" />
</p>

## Dự án Tìm kiếm (Search Project)

- **Thuật toán triển khai**:
  - Depth-First Search (DFS)
  - Breadth-First Search (BFS)
  - Uniform Cost Search (UCS)
  - A\* Search
  - Iterative Deepening Search (IDS)
  - Enforced Hill Climbing (EHC)
- **Bài toán Capsule Search**:
  - Tạo `CapsuleSearchProblem` và `CapsuleSearchAgent` để Pacman ăn capsule trước, sau đó thu thập hết thức ăn.
  - Heuristic tùy chỉnh (`capsuleProblemHeuristic`) dựa trên khoảng cách Manhattan.

## Cài đặt và Chạy

1. Cài Python 2.7
2. Chạy các lệnh kiểm tra:

   ```bash
   python pacman.py -l tinyMaze -p SearchAgent -a fn=dfs
   python pacman.py -l capsuleSearch -p CapsuleSearchAgent -a fn=astar,prob=CapsuleSearchProblem,heuristic=capsuleProblemHeuristic
   ```

## 
