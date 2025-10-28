"""워크플로우 예시 및 실행 코드"""

import asyncio

from database.graph.edge import Edge
from database.graph.vertex import Vertex
from helpers.engine.workflow_engine import WorkflowEngine
from helpers.node.node_base import NodeInputOutputType


async def create_and_run_condition_workflow():
    """조건문 노드를 이용한 워크플로우 생성 및 실행 예시"""

    # 1. 워크플로우 엔진 생성
    engine = WorkflowEngine()

    # 2. 노드(Vertex) 생성
    # 노드 1: 텍스트 입력 노드
    input_node = Vertex(
        id=1,
        graph_id=1,
        type="TEXT_INPUT",
        properties={"initial_text": "user123"},
    )

    # 노드 2: 조건 노드 (입력값이 admin인지 확인)
    condition_node = Vertex(
        id=2,
        graph_id=1,
        type="CONDITION",
        properties={"condition": "value == 'admin'", "operator": "=="},
    )

    # 노드 3: JSON 출력 노드
    output_node = Vertex(id=3, graph_id=1, type="JSON_OUTPUT", properties={})

    vertices = [input_node, condition_node, output_node]

    # 3. 엣지(연결) 생성
    # 입력 노드 -> 조건 노드 (text -> value)
    edge1 = Edge(
        id=1,
        graph_id=1,
        source_id=1,
        target_id=2,
        type="data_flow",
        source_properties={
            "id": "port1",
            "name": "text",
            "type": NodeInputOutputType.TEXT.value,
            "description": "입력된 텍스트",
        },
        target_properties={
            "id": "port2",
            "name": "value",
            "type": NodeInputOutputType.TEXT.value,
            "description": "비교할 값",
        },
    )

    # 조건 노드 -> 출력 노드
    edge2 = Edge(
        id=2,
        graph_id=1,
        source_id=2,
        target_id=3,
        type="data_flow",
        source_properties={
            "id": "port3",
            "name": "true",
            "type": NodeInputOutputType.BOOLEAN.value,
            "description": "조건이 참일 때",
        },
        target_properties={
            "id": "port4",
            "name": "data",
            "type": NodeInputOutputType.JSON.value,
            "description": "출력할 데이터",
        },
    )

    edges = [edge1, edge2]

    # 4. 워크플로우 로드
    print("워크플로우 로드 중...")
    success = await engine.load(vertices, edges)
    if not success:
        print("워크플로우 로드 실패!")
        return

    print("워크플로우 로드 완료!")
    print(f"노드 수: {len(vertices)}")
    print(f"엣지 수: {len(edges)}")

    # 5. 워크플로우 실행
    print("\n워크플로우 실행 중...")
    print("-" * 50)

    # 초기 입력 설정
    initial_inputs = {
        "text": "admin",  # admin인 경우
    }

    result = await engine.start(initial_inputs=initial_inputs)

    # 6. 실행 결과 출력
    print("\n실행 결과:")
    print("-" * 50)
    print(f"성공 여부: {result.success}")
    print(f"실행 시간: {result.execution_time:.2f}초")
    print(f"실행 순서: {result.execution_order}")

    if result.errors:
        print(f"에러 수: {len(result.errors)}")
        for error in result.errors:
            print(f"  - {error}")

    print("\n노드별 결과:")
    for node_id, node_result in result.node_results.items():
        print(f"\n노드 {node_id}:")
        if isinstance(node_result, dict):
            for key, value in node_result.items():
                if key != "node_type" and key != "prompt" and key != "model":
                    print(f"  {key}: {str(value)[:100]}...")  # 처음 100자만 출력
                else:
                    print(f"  {key}: {value}")

    print("\n전체 워크플로우 상태:")
    print("-" * 50)
    workflow_status = engine.get_workflow_status()
    print(f"총 노드 수: {workflow_status['total_nodes']}")

    return result


async def create_and_run_split_workflow():
    """텍스트 분할 워크플로우 예시"""

    engine = WorkflowEngine()

    # 1. 입력 노드
    input_node = Vertex(
        id=1,
        graph_id=2,
        type="TEXT_INPUT",
        properties={"initial_text": "사과,바나나,오렌지,딸기,포도"},
    )

    # 2. 분할 노드
    split_node = Vertex(id=2, graph_id=2, type="SPLIT", properties={"separator": ","})

    # 3. 출력 노드
    output_node = Vertex(id=3, graph_id=2, type="JSON_OUTPUT", properties={})

    vertices = [input_node, split_node, output_node]

    # 엣지 생성
    edge1 = Edge(
        id=1,
        graph_id=2,
        source_id=1,
        target_id=2,
        type="data_flow",
        source_properties={
            "id": "port1",
            "name": "text",
            "type": NodeInputOutputType.TEXT.value,
            "description": "입력된 텍스트",
        },
        target_properties={
            "id": "port2",
            "name": "data",
            "type": NodeInputOutputType.TEXT.value,
            "description": "분할할 데이터",
        },
    )

    edge2 = Edge(
        id=2,
        graph_id=2,
        source_id=2,
        target_id=3,
        type="data_flow",
        source_properties={
            "id": "port3",
            "name": "split_data",
            "type": NodeInputOutputType.ARRAY.value,
            "description": "분할된 데이터 배열",
        },
        target_properties={
            "id": "port4",
            "name": "data",
            "type": NodeInputOutputType.JSON.value,
            "description": "출력할 JSON 데이터",
        },
    )

    edges = [edge1, edge2]

    # 워크플로우 로드
    print("워크플로우 로드 중...")
    await engine.load(vertices, edges)
    print("워크플로우 로드 완료!")

    # 워크플로우 실행
    print("\n워크플로우 실행 중...")
    print("-" * 50)

    initial_inputs = {"text": "Python,JavaScript,Java,Go,Rust"}

    result = await engine.start(initial_inputs=initial_inputs)

    # 결과 출력
    print("\n실행 결과:")
    print("-" * 50)
    print(f"성공 여부: {result.success}")
    print(f"실행 시간: {result.execution_time:.2f}초")

    if result.node_results:
        print("\n노드별 결과:")
        for node_id, node_result in result.node_results.items():
            print(f"노드 {node_id}: {node_result}")

    return result


async def main():
    """메인 실행 함수"""
    print("=" * 70)
    print("워크플로우 예시 실행")
    print("=" * 70)

    print("\n[예시 1: 조건문 노드를 이용한 워크플로우]")
    print("=" * 70)
    try:
        await create_and_run_condition_workflow()
    except Exception as e:
        print(f"에러 발생: {e}")
        import traceback

        traceback.print_exc()

    print("\n\n[예시 2: 텍스트 분할 워크플로우]")
    print("=" * 70)
    try:
        await create_and_run_split_workflow()
    except Exception as e:
        print(f"에러 발생: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 70)
    print("모든 워크플로우 실행 완료!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
