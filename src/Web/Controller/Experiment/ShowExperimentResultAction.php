<?php

declare(strict_types=1);

namespace Genre\Web\Controller\Experiment;

use Genre\Domain\Service\ExperimentService;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Twig\Environment;

class ShowExperimentResultAction
{
    private ExperimentService $experimentService;
    private Environment $twig;

    public function __construct(ExperimentService $experimentService, Environment $twig)
    {
        $this->experimentService = $experimentService;
        $this->twig = $twig;
    }

    public function __invoke(Request $request): Response
    {
        $paramsArray = $request->request->all();
        $result = $this->experimentService->getExperimentResult($paramsArray);
        return new Response($this->twig->render('experiment/result.html.twig', ['result' => $result]));
    }
}
