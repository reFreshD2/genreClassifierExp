<?php

declare(strict_types=1);

namespace Genre\Web\Controller\MusicMetrics;

use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Genre\Domain\MusicMetrics\Repository\MusicMetricsRepository;
use Genre\Domain\Service\ParserService;
use Genre\Domain\Service\UploadService;
use Symfony\Component\HttpFoundation\RedirectResponse;
use Symfony\Component\HttpFoundation\Request;

class UploadAction
{
    private UploadService $uploadService;
    private ParserService $parserService;
    private MusicMetricsRepository $musicMetricsRepository;

    public function __construct(
        UploadService $uploadService,
        ParserService $parserService,
        MusicMetricsRepository $musicMetricsRepository
    ) {
        $this->uploadService = $uploadService;
        $this->parserService = $parserService;
        $this->musicMetricsRepository = $musicMetricsRepository;
    }

    /**
     * @throws OptimisticLockException
     * @throws ORMException
     */
    public function __invoke(Request $request): RedirectResponse
    {
        $files = $request->files->get('audio');
        $genre = $request->request->get('genre');
        foreach ($files as $file) {
            if ($file->getClientMimeType( ) !== 'audio/wav') {
                continue;
            }
            $audioFile = $this->uploadService->upload($file);
            if (!$audioFile || !$audioFile->getPath()) {
                continue;
            }
            $musicMetrics = $this->parserService->parse($audioFile);
            $musicMetrics->setGenre($genre);
            $this->musicMetricsRepository->save($musicMetrics);
        }

        return new RedirectResponse('/musicMetrics');
    }
}
