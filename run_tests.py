#!/usr/bin/env python3
"""
테스트 실행 스크립트
create_simple_workflow() 함수에 대한 테스트를 실행합니다.
"""

import os
import subprocess
import sys


def run_tests():
    """테스트 실행"""
    print("🧪 create_simple_workflow() 테스트 실행 중...")
    print("=" * 50)

    # 현재 디렉토리를 프로젝트 루트로 설정
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)

    try:
        # pytest 실행
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/test_workflow_router.py",
                "-v",  # verbose 출력
                "--tb=short",  # 짧은 traceback
                "--color=yes",  # 컬러 출력
            ],
            capture_output=False,
            text=True,
        )

        if result.returncode == 0:
            print("\n✅ 모든 테스트가 성공적으로 통과했습니다!")
        else:
            print("\n❌ 일부 테스트가 실패했습니다.")

        return result.returncode

    except FileNotFoundError:
        print("❌ pytest가 설치되지 않았습니다.")
        print("다음 명령어로 설치하세요: pip install pytest")
        return 1
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류가 발생했습니다: {e}")
        return 1


def run_specific_test():
    """특정 테스트만 실행"""
    print("🎯 create_simple_workflow 성공 케이스만 테스트...")
    print("=" * 50)

    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/test_workflow_router.py::TestCreateSimpleWorkflow::test_create_simple_workflow_success",
                "-v",
                "--tb=short",
                "--color=yes",
            ],
            capture_output=False,
            text=True,
        )

        return result.returncode

    except Exception as e:
        print(f"❌ 테스트 실행 중 오류가 발생했습니다: {e}")
        return 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--specific":
        exit_code = run_specific_test()
    else:
        exit_code = run_tests()

    sys.exit(exit_code)
