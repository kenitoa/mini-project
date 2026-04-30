# BFS

BFS는 Breadth First Search의 줄임말이고, 한국어로는 너비 우선 탐색이라고 부른다.

BFS는 그래프나 트리에서 시작 정점과 가까운 정점부터 차례대로 방문하는 탐색 방법이다.

한 방향으로 깊게 들어가는 DFS와 달리, BFS는 현재 위치에서 갈 수 있는 곳들을 먼저 모두 확인한 뒤 다음 단계로 넘어간다.

즉, 가까운 곳부터 넓게 퍼져 나가면서 탐색하는 방식이다.

BFS는 보통 다음 자료 구조를 사용해 구현한다.

```text
큐
```

큐는 먼저 들어온 값이 먼저 나가는 자료 구조이다.

```text
enqueue: 큐에 넣기
dequeue: 큐에서 꺼내기
```

먼저 발견한 정점부터 차례대로 처리해야 하므로 BFS에서는 큐가 매우 중요하다.

## 핵심 생각

예를 들어 다음과 같은 그래프가 있다고 하자.

```text
A -- B -- D
|    |
C    E
|
F
```

이 그래프를 연결 관계로 나타내면 다음과 같다.

```text
A: B, C
B: A, D, E
C: A, F
D: B
E: B
F: C
```

`A`에서 시작해서 BFS를 한다면 `A`와 가까운 정점부터 방문한다.

예를 들어 `A`의 이웃을 `B`, `C` 순서로 확인한다고 하자.

```text
A에서 시작
A와 가까운 B, C를 확인
B에서 갈 수 있는 D, E를 확인
C에서 갈 수 있는 F를 확인
```

방문 순서는 다음과 같을 수 있다.

```text
A -> B -> C -> D -> E -> F
```

즉, BFS는 시작 정점에서 거리가 `1`인 정점들을 먼저 보고, 그 다음 거리가 `2`인 정점들을 보는 식으로 탐색한다.

## 그래프에서 사용하는 말

BFS를 이해하려면 그래프에서 자주 사용하는 말을 알아두면 좋다.

```text
정점 또는 노드: 데이터가 있는 지점
간선: 정점과 정점을 연결하는 선
인접 정점: 현재 정점에서 바로 갈 수 있는 정점
방문: 어떤 정점에 도착해서 확인했다는 뜻
방문 체크: 이미 방문한 정점을 다시 방문하지 않도록 표시하는 것
거리: 시작 정점에서 어떤 정점까지 가는 데 필요한 간선의 수
```

예를 들어 다음 그래프에서:

```text
A -- B
|
C
```

`A`의 인접 정점은 `B`와 `C`이다.

`A`에서 `B`까지의 거리는 `1`이고, `A`에서 `C`까지의 거리도 `1`이다.

BFS는 이런 가까운 정점들을 먼저 방문한다.

## 왜 방문 체크가 필요한가

그래프에는 사이클이 있을 수 있다.

사이클은 다시 자기 자신 쪽으로 돌아올 수 있는 길이다.

예를 들어:

```text
A -- B
|    |
C -- D
```

`A`에서 `B`로 가고, `B`에서 `D`로 가고, `D`에서 `C`로 가고, `C`에서 다시 `A`로 갈 수 있다.

방문 체크를 하지 않으면 같은 정점을 큐에 계속 넣을 수 있다.

```text
A -> B -> C -> D -> A -> B -> C -> D -> ...
```

그래서 BFS에서는 보통 `visited`라는 집합이나 배열을 사용한다.

```text
visited = 이미 방문한 정점들
```

어떤 정점을 발견하면 `visited`에 기록한다.

그리고 다음 정점을 큐에 넣기 전에 이미 방문했는지 확인한다.

```text
이미 방문했다면 큐에 넣지 않는다.
방문하지 않았다면 방문 표시를 하고 큐에 넣는다.
```

## 큐를 사용하는 이유

BFS는 먼저 발견한 정점부터 먼저 처리해야 한다.

그래야 가까운 정점부터 차례대로 탐색할 수 있다.

큐는 먼저 들어온 값이 먼저 나오는 자료 구조이다.

```text
먼저 들어온 정점 -> 먼저 처리
나중에 들어온 정점 -> 나중에 처리
```

예를 들어 `A`에서 `B`, `C`를 발견했다면 먼저 `B`를 처리하고 그 다음 `C`를 처리한다.

```text
queue = [B, C]
```

`B`를 꺼내서 처리한다.

```text
dequeue -> B
queue = [C]
```

`B`에서 새로 발견한 `D`, `E`를 뒤에 넣는다.

```text
queue = [C, D, E]
```

이렇게 하면 `C`가 `D`, `E`보다 먼저 처리된다.

그래서 `A`와 더 가까운 정점들이 먼저 방문된다.

## BFS 의사코드

가장 기본적인 BFS는 시작 정점에서 갈 수 있는 모든 정점을 방문한다.

```text
bfs(그래프, 시작 정점):
    큐를 만든다
    시작 정점을 방문했다고 표시한다
    시작 정점을 큐에 넣는다

    큐가 비어 있지 않은 동안 반복한다:
        큐에서 정점을 하나 꺼낸다
        꺼낸 정점을 처리한다

        현재 정점과 연결된 다음 정점들을 하나씩 확인한다:
            다음 정점을 아직 방문하지 않았다면:
                다음 정점을 방문했다고 표시한다
                다음 정점을 큐에 넣는다
```

여기서 정점을 처리한다는 말은 문제에 따라 달라진다.

```text
정점 이름 출력하기
정점 개수 세기
목표 정점인지 확인하기
거리 기록하기
```

## 조금 더 코드처럼 쓴 의사코드

```text
function bfs(graph, start):
    queue = empty queue
    visited = empty set

    add start to visited
    enqueue start to queue

    while queue is not empty:
        current = dequeue from queue
        print current

        for each next in graph[current]:
            if next is not in visited:
                add next to visited
                enqueue next to queue
```

이 코드는 `start`에서 시작해서 연결된 모든 정점을 너비 우선으로 방문한다.

`visited`는 이미 방문한 정점을 저장한다.

`queue`는 앞으로 방문할 정점을 순서대로 저장한다.

## 목표 값을 찾는 BFS 의사코드

BFS는 단순히 모든 정점을 방문할 수도 있고, 특정 목표 정점을 찾는 데 사용할 수도 있다.

예를 들어 `target`을 찾는 BFS는 다음처럼 쓸 수 있다.

```text
function bfs_search(graph, start, target):
    queue = empty queue
    visited = empty set

    add start to visited
    enqueue start to queue

    while queue is not empty:
        current = dequeue from queue

        if current == target:
            return current

        for each next in graph[current]:
            if next is not in visited:
                add next to visited
                enqueue next to queue

    return null
```

현재 정점이 찾는 정점이라면 바로 반환한다.

그렇지 않다면 현재 정점과 연결된 정점들을 큐에 넣고, 먼저 들어온 정점부터 차례대로 확인한다.

끝까지 찾지 못하면 `null`을 반환한다.

## 흐름을 쉽게 떠올려보기

BFS는 이렇게 생각하면 쉽다.

```text
1. 시작 정점을 정한다.
2. 시작 정점을 방문했다고 표시하고 큐에 넣는다.
3. 큐에서 정점을 하나 꺼낸다.
4. 현재 정점을 처리한다.
5. 현재 정점에서 갈 수 있는 정점들을 확인한다.
6. 아직 방문하지 않은 정점들을 방문 표시하고 큐에 넣는다.
7. 큐가 빌 때까지 반복한다.
```

즉, BFS는 먼저 발견한 정점부터 차례대로 처리하면서 가까운 곳부터 넓게 퍼져 나가는 방식이다.

## 예시

다음 그래프가 있다고 하자.

```text
A: B, C
B: A, D, E
C: A, F
D: B
E: B
F: C
```

`A`에서 시작해서 모든 정점을 BFS로 방문한다고 하자.

```text
bfs(graph, A)
```

이웃 정점을 적힌 순서대로 확인하면 흐름은 다음과 같다.

```text
queue = [A]

A 방문
B, C를 큐에 넣음
queue = [B, C]

B 방문
D, E를 큐에 넣음
queue = [C, D, E]

C 방문
F를 큐에 넣음
queue = [D, E, F]

D 방문
queue = [E, F]

E 방문
queue = [F]

F 방문
queue = []
```

방문 순서는 다음과 같다.

```text
A -> B -> C -> D -> E -> F
```

## 목표 정점을 찾는 예시

같은 그래프에서 `E`를 찾는다고 하자.

```text
bfs_search(graph, A, E)
```

탐색 흐름은 다음과 같다.

```text
A == E ? 아니오
B, C를 큐에 넣음

B == E ? 아니오
D, E를 큐에 넣음

C == E ? 아니오
F를 큐에 넣음

D == E ? 아니오

E == E ? 예
```

`E`를 찾았으므로 탐색을 종료한다.

```text
return E
```

목표를 찾는 문제라면 큐에 남은 정점이 있더라도 찾는 순간 바로 종료할 수 있다.

## 찾는 정점이 없는 예시

다음 그래프에서 `G`를 찾는다고 하자.

```text
A: B, C
B: A, D, E
C: A, F
D: B
E: B
F: C
```

```text
bfs_search(graph, A, G)
```

BFS는 `A`에서 갈 수 있는 모든 정점을 확인한다.

```text
A 방문
B 방문
C 방문
D 방문
E 방문
F 방문
```

하지만 `G`는 그래프 안에 없다.

따라서 끝까지 찾지 못했다는 값을 반환한다.

```text
return null
```

## 종료 조건

BFS가 끝나는 경우는 크게 두 가지다.

첫 번째는 원하는 정점을 찾은 경우다.

```text
if current == target:
    return current
```

목표를 찾았다면 더 이상 다른 정점을 확인할 필요가 없으므로 바로 종료한다.

두 번째는 큐가 비어 있는 경우다.

```text
while queue is not empty:
```

큐가 비었다는 것은 시작 정점에서 갈 수 있는 모든 정점을 확인했다는 뜻이다.

이때까지 목표를 찾지 못했다면 찾는 정점이 없다고 판단한다.

```text
return null
```

## 빈 그래프인 경우

그래프에 정점이 하나도 없다면 BFS를 시작할 정점도 없다.

```text
graph = {}
```

이 경우에는 탐색을 실행할 수 없으므로 바로 찾지 못했다고 처리한다.

```text
return null
```

실제 코드에서는 BFS를 시작하기 전에 시작 정점이 그래프 안에 있는지 확인하는 것이 좋다.

```text
if start is not in graph:
    return null
```

## 시작 정점만 있는 경우

그래프에 시작 정점만 있고 연결된 정점이 없을 수도 있다.

```text
A: empty
```

이때 `A`에서 BFS를 시작하면 `A`만 방문한다.

```text
A 방문
```

찾는 정점이 `A`라면 성공이다.

```text
bfs_search(graph, A, A)
return A
```

찾는 정점이 다른 값이라면 큐가 비고 탐색이 끝난다.

```text
bfs_search(graph, A, B)
return null
```

## 연결되지 않은 그래프

그래프는 모든 정점이 하나로 연결되어 있지 않을 수도 있다.

예를 들어:

```text
A -- B

C -- D
```

이 그래프는 두 부분으로 나뉘어 있다.

```text
A: B
B: A
C: D
D: C
```

`A`에서 BFS를 시작하면 `A`와 `B`만 방문할 수 있다.

```text
A -> B
```

`C`와 `D`는 `A`에서 갈 수 없으므로 방문되지 않는다.

그래프 전체의 모든 정점을 방문하고 싶다면 모든 정점을 시작점 후보로 확인해야 한다.

```text
function bfs_all(graph):
    visited = empty set

    for each node in graph:
        if node is not in visited:
            queue = empty queue
            add node to visited
            enqueue node to queue

            while queue is not empty:
                current = dequeue from queue
                print current

                for each next in graph[current]:
                    if next is not in visited:
                        add next to visited
                        enqueue next to queue
```

이 방식은 연결되지 않은 그래프에서도 모든 정점을 방문할 수 있다.

## 큐로 구현하는 BFS

BFS는 큐로 구현하는 것이 가장 일반적이다.

```text
function bfs(graph, start):
    queue = empty queue
    visited = empty set

    add start to visited
    enqueue start to queue

    while queue is not empty:
        current = dequeue from queue
        print current

        for each next in graph[current]:
            if next is not in visited:
                add next to visited
                enqueue next to queue
```

큐 BFS에서는 방문할 정점을 큐에 넣어 두고, 가장 먼저 넣은 정점부터 꺼내서 방문한다.

이 구조 덕분에 시작 정점에서 가까운 정점부터 순서대로 처리된다.

## 방문 표시를 언제 해야 하는가

BFS에서는 보통 정점을 큐에 넣을 때 방문 표시를 한다.

```text
if next is not in visited:
    add next to visited
    enqueue next to queue
```

이렇게 하면 같은 정점이 큐에 여러 번 들어가는 것을 막을 수 있다.

만약 큐에서 꺼낼 때 방문 표시를 한다면, 여러 정점이 같은 정점을 동시에 발견했을 때 그 정점이 큐에 중복으로 들어갈 수 있다.

예를 들어:

```text
A: B, C
B: D
C: D
```

`B`도 `D`를 발견하고, `C`도 `D`를 발견할 수 있다.

큐에 넣을 때 방문 표시를 하면 `D`는 한 번만 큐에 들어간다.

## 거리 계산하는 BFS

BFS는 가중치가 없는 그래프에서 시작 정점으로부터의 최단 거리를 구할 때 자주 사용된다.

가중치가 없다는 말은 모든 간선의 이동 비용이 같다는 뜻이다.

예를 들어 모든 길의 비용이 `1`이라고 생각하면 된다.

```text
A -- B -- D
|
C
```

`A`에서 각 정점까지의 최단 거리는 다음과 같다.

```text
A까지 거리: 0
B까지 거리: 1
C까지 거리: 1
D까지 거리: 2
```

BFS는 가까운 정점부터 방문하므로, 어떤 정점을 처음 방문했을 때의 거리가 그 정점까지의 최단 거리이다.

거리 계산 의사코드는 다음과 같다.

```text
function bfs_distance(graph, start):
    queue = empty queue
    distance = empty map

    distance[start] = 0
    enqueue start to queue

    while queue is not empty:
        current = dequeue from queue

        for each next in graph[current]:
            if next is not in distance:
                distance[next] = distance[current] + 1
                enqueue next to queue

    return distance
```

여기서는 `distance`가 방문 기록 역할도 한다.

이미 거리가 기록된 정점은 이미 방문한 정점이라고 볼 수 있다.

## 최단 경로를 저장하는 BFS

BFS는 최단 거리뿐 아니라 실제 최단 경로도 저장할 수 있다.

이를 위해 각 정점을 처음 발견했을 때, 어느 정점에서 왔는지를 기록한다.

```text
parent[next] = current
```

예를 들어 `A`에서 `F`까지의 최단 경로를 찾고 싶다고 하자.

```text
A: B, C
B: D, E
C: F
D: empty
E: empty
F: empty
```

최단 경로를 저장하는 BFS는 다음처럼 생각할 수 있다.

```text
function bfs_path(graph, start, target):
    queue = empty queue
    visited = empty set
    parent = empty map

    add start to visited
    parent[start] = null
    enqueue start to queue

    while queue is not empty:
        current = dequeue from queue

        if current == target:
            return make_path(parent, target)

        for each next in graph[current]:
            if next is not in visited:
                add next to visited
                parent[next] = current
                enqueue next to queue

    return null
```

`target`을 찾으면 `parent`를 거꾸로 따라가면서 경로를 만들 수 있다.

```text
F의 부모: C
C의 부모: A
A의 부모: null
```

따라서 경로는 다음과 같다.

```text
A -> C -> F
```

## 레벨 단위 탐색

BFS는 레벨 단위로 생각할 수 있다.

시작 정점을 레벨 `0`이라고 하면, 시작 정점과 바로 연결된 정점들은 레벨 `1`이다.

그 다음 정점들은 레벨 `2`가 된다.

```text
level 0: A
level 1: B, C
level 2: D, E, F
```

이런 성질 때문에 BFS는 다음과 같은 문제에 잘 맞는다.

```text
시작점에서 몇 번 이동해야 도착할 수 있는가?
가장 적은 이동 횟수는 얼마인가?
가장 가까운 목표는 무엇인가?
```

예를 들어 미로에서 상하좌우로 한 칸씩만 이동할 수 있다면, BFS로 출구까지의 최소 이동 횟수를 구할 수 있다.

## 트리에서의 BFS

트리에서 BFS는 루트에서 가까운 노드부터 방문한다.

다음과 같은 트리가 있다고 하자.

```text
      A
     / \
    B   C
   / \   \
  D   E   F
```

트리에서 BFS를 하면 레벨 순서대로 방문한다.

```text
A -> B -> C -> D -> E -> F
```

이런 순회를 레벨 순회라고도 부른다.

```text
level 0: A
level 1: B, C
level 2: D, E, F
```

트리의 높이, 각 레벨의 노드 개수, 가장 가까운 리프 노드 등을 구할 때 BFS가 유용하다.

## 인접 리스트와 인접 행렬

BFS에서 그래프를 저장하는 대표적인 방법은 두 가지이다.

```text
인접 리스트
인접 행렬
```

인접 리스트는 각 정점마다 연결된 정점 목록을 저장한다.

```text
A: B, C
B: A, D
C: A
D: B
```

연결된 정점만 저장하므로 보통 공간을 적게 사용한다.

인접 행렬은 정점과 정점이 연결되어 있는지를 표처럼 저장한다.

```text
    A B C D
A   0 1 1 0
B   1 0 0 1
C   1 0 0 0
D   0 1 0 0
```

두 정점이 연결되어 있는지 빠르게 확인할 수 있지만, 정점이 많으면 공간을 많이 사용할 수 있다.

BFS에서는 보통 인접 리스트를 많이 사용한다.

## 시간 복잡도

BFS의 시간 복잡도는 그래프를 어떻게 저장했는지에 따라 다르게 볼 수 있다.

인접 리스트를 사용하면 각 정점과 각 간선을 한 번씩 확인한다.

```text
O(V + E)
```

여기서 `V`는 정점의 개수이고, `E`는 간선의 개수이다.

정점마다 방문 체크를 하고, 각 정점의 인접 정점을 확인하기 때문이다.

인접 행렬을 사용하면 각 정점에서 다른 모든 정점과 연결되어 있는지 확인해야 할 수 있다.

```text
O(V^2)
```

그래서 BFS의 시간 복잡도는 보통 다음처럼 말한다.

```text
인접 리스트: O(V + E)
인접 행렬: O(V^2)
```

트리에서는 간선의 수가 보통 정점 수보다 하나 적다.

그래서 트리 BFS는 보통 다음처럼 생각할 수 있다.

```text
O(n)
```

## 공간 복잡도

BFS는 방문 기록이 필요하다.

정점이 `V`개라면 방문 기록에 최대 `V`개의 정점이 저장될 수 있다.

```text
visited: O(V)
```

또 앞으로 방문할 정점을 저장하는 큐가 필요하다.

큐에는 한 번에 여러 정점이 들어갈 수 있다.

최악의 경우 큐에 최대 `V`개의 정점이 들어갈 수 있다.

```text
queue: O(V)
```

그래서 BFS의 공간 복잡도는 보통 다음과 같다.

```text
O(V)
```

트리에서 정점 수를 `n`이라고 하면 다음처럼 말할 수 있다.

```text
O(n)
```

## 장점

```text
가까운 정점부터 차례대로 탐색할 수 있다.
가중치가 없는 그래프에서 최단 거리를 구할 수 있다.
레벨 단위 탐색에 적합하다.
큐를 사용하면 구현 흐름이 명확하다.
그래프와 트리 모두에 사용할 수 있다.
시작점에서 가장 가까운 목표를 찾는 문제에 좋다.
```

## 단점

```text
큐에 많은 정점이 들어갈 수 있어 메모리를 많이 사용할 수 있다.
가중치가 있는 그래프의 최단 경로에는 그대로 사용할 수 없다.
모든 가까운 정점을 저장하면서 진행하므로 공간 사용량이 커질 수 있다.
깊은 경로 하나만 빠르게 확인하고 싶은 문제에는 DFS가 더 자연스러울 수 있다.
방문 체크를 하지 않으면 사이클에서 무한 반복될 수 있다.
```

## DFS와 비교

DFS는 Depth First Search의 줄임말이고, 깊이 우선 탐색이라고 부른다.

BFS가 가까운 정점부터 넓게 확인하는 방식이라면, DFS는 한 방향으로 갈 수 있는 만큼 깊게 들어가는 방식이다.

```text
BFS: 가까운 곳부터 넓게 본다.
DFS: 깊게 들어간다.
```

예를 들어 다음 그래프가 있다고 하자.

```text
A: B, C
B: D, E
C: F
```

BFS의 방문 순서는 다음과 같다.

```text
A -> B -> C -> D -> E -> F
```

DFS의 방문 순서는 다음과 같을 수 있다.

```text
A -> B -> D -> E -> C -> F
```

가중치가 없는 그래프에서 최단 거리를 찾는 문제는 보통 BFS가 더 적합하다.

반면 가능한 경로를 끝까지 탐색하거나, 모든 경우를 시도하는 문제는 DFS가 더 자연스럽게 쓰이는 경우가 많다.

```text
BFS가 좋은 경우: 가까운 정점부터 탐색, 최단 거리 탐색
DFS가 좋은 경우: 경로 탐색, 백트래킹, 모든 경우 탐색
```

## 언제 사용하면 좋은가

BFS는 다음과 같은 상황에서 사용하기 좋다.

```text
그래프의 모든 정점을 가까운 순서대로 방문하고 싶을 때
두 정점 사이의 최단 거리를 구하고 싶을 때
가중치가 없는 그래프에서 최소 이동 횟수를 구하고 싶을 때
미로에서 출구까지 가장 짧은 길을 찾고 싶을 때
시작점에서 가장 가까운 목표를 찾고 싶을 때
트리를 레벨 순서대로 방문하고 싶을 때
연결 요소의 개수를 구할 때
네트워크에서 몇 단계 안에 도달 가능한지 확인할 때
```

## 주의할 점

BFS를 사용할 때 가장 중요한 것은 방문 체크이다.

그래프에 사이클이 있으면 같은 정점을 계속 큐에 넣을 수 있기 때문이다.

```text
if next is not in visited:
    add next to visited
    enqueue next to queue
```

또 BFS는 가중치가 없는 그래프의 최단 거리에는 적합하지만, 가중치가 있는 그래프에서는 조심해야 한다.

간선마다 비용이 다르다면 단순 BFS로는 최단 비용을 보장할 수 없다.

이런 경우에는 다익스트라 알고리즘 같은 다른 방법을 사용해야 한다.

방문 순서가 중요한 문제라면 인접 정점의 순서도 확인해야 한다.

```text
A: B, C
A: C, B
```

두 경우 모두 같은 그래프처럼 보일 수 있지만 BFS 방문 순서는 달라진다.

## 한 문장 요약

BFS는 그래프나 트리에서 시작 정점과 가까운 정점부터 차례대로 방문하며, 큐를 사용해 넓게 퍼져 나가는 너비 우선 탐색 알고리즘이다.

## 알고리즘 흐름도

아래 흐름은 BFS를 언제 어디서든 다시 만들 수 있게 정리한 것이다.

```text
시작
  |
  v
그래프와 시작 정점을 받는다
  |
  v
큐를 만든다
  |
  v
시작 정점을 방문했다고 표시하고 큐에 넣는다
  |
  v
큐가 비어 있는가?
  |
  +-- 예 --> 탐색을 종료한다
  |
  +-- 아니오
        |
        v
      큐에서 정점을 하나 꺼낸다
        |
        v
      현재 정점을 처리한다
        |
        v
      현재 정점과 연결된 다음 정점들을 확인한다
        |
        v
      다음 정점을 이미 방문했는가?
        |
        +-- 예 --> 다른 다음 정점을 확인한다
        |
        +-- 아니오
              |
              v
            다음 정점을 방문했다고 표시한다
              |
              v
            다음 정점을 큐에 넣는다
              |
              v
            다시 큐가 비어 있는지 확인한다
```

## 더 짧게 외우는 흐름

```text
1. 시작 정점을 정한다.
2. 시작 정점을 방문 표시하고 큐에 넣는다.
3. 큐에서 정점을 하나 꺼낸다.
4. 현재 정점과 연결된 정점들을 확인한다.
5. 방문하지 않은 정점을 방문 표시하고 큐에 넣는다.
6. 큐가 빌 때까지 반복한다.
```

## 머릿속 결정 순서

BFS를 코드로 만들 때는 이 질문 순서만 기억하면 된다.

```text
어디에서 시작할 것인가?
  -> start 정하기

그래프는 어떻게 저장되어 있는가?
  -> 인접 리스트 또는 인접 행렬 확인

무엇으로 방문 순서를 관리할 것인가?
  -> queue 만들기

시작 정점을 어떻게 처리할 것인가?
  -> visited에 기록하고 queue에 넣기

큐에서 무엇을 꺼낼 것인가?
  -> 가장 먼저 들어온 정점 꺼내기

현재 정점에서 어디로 갈 수 있는가?
  -> 인접 정점 확인하기

다음 정점을 이미 방문했는가?
  -> 방문했다면 건너뛰기

방문하지 않았다면 무엇을 할 것인가?
  -> visited에 기록하고 queue에 넣기

언제 끝낼 것인가?
  -> 목표를 찾거나 queue가 비었을 때

끝까지 없으면 어떻게 할 것인가?
  -> null 같은 실패 값을 반환
```
