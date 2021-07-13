<?php

declare(strict_types=1);

namespace Genre\Web\Controller\MusicMetrics;

use Genre\Domain\MusicMetrics\Repository\MusicMetricsRepository;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Twig\Environment;

class ShowMusicMetricsAction
{
    private MusicMetricsRepository $musicMetricsRepository;
    private Environment $twig;

    public function __construct(MusicMetricsRepository $musicMetricsRepository, Environment $twig)
    {
        $this->musicMetricsRepository = $musicMetricsRepository;
        $this->twig = $twig;
    }

    public function __invoke(Request $request): Response
    {
        $genres = $this->musicMetricsRepository->getGenre();
        if (!$request->query->has('genre')) {
            $view = $this->musicMetricsRepository->getView();
        } else {
            $view = $this->musicMetricsRepository->findBy(['genre' => $request->query->get('genre')]);
        }
        return new Response($this->twig->render('musicMetrics/index.html.twig', ['records' => $view, 'genres' => $genres]));
    }
}
