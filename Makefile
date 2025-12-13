test-cov: ## run tests with coverage
	@pytest tests --junitxml=`pwd`/~build/pytest.xml -vv \
        --cov-report=xml:`pwd`/~build/coverage.xml --cov-report=html --cov-report=term \
        --cov-config=tests/.coveragerc \
        --cov=jmespath_filters || true
	@if [ "${BROWSERCMD}" != "" ]; then \
    	"${BROWSERCMD}" `pwd`/~build/coverage/index.html ; \
    fi
