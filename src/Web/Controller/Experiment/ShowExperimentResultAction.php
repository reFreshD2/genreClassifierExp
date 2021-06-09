<?php

declare(strict_types=1);

namespace Genre\Web\Controller\Experiment;

use Genre\Domain\Service\ExperimentService;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

class ShowExperimentResultAction
{
    private ExperimentService $experimentService;

    public function __construct(ExperimentService $experimentService)
    {
        $this->experimentService = $experimentService;
    }

    public function __invoke(Request $request): Response
    {
        $paramsArray = $request->request->all();
        $result = $this->experimentService->getExperimentResult($paramsArray);
        return new Response();
    }
}
