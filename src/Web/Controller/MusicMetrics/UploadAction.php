<?php

declare(strict_types=1);

namespace Genre\Web\Controller\MusicMetrics;

use Genre\Domain\Service\ParserService;
use Genre\Domain\Service\UploadService;
use Symfony\Component\HttpFoundation\Request;

class UploadAction
{
    private UploadService $uploadService;
    private ParserService $parserService;

    public function __construct(UploadService $uploadService, ParserService $parserService)
    {
        $this->uploadService = $uploadService;
        $this->parserService = $parserService;
    }

    public function __invoke(Request $request)
    {
        $files = $request->files->get('audio');
        foreach ($files as $file) {
            if ($file->getClientMimeType( ) !== 'audio/wav') {
                continue;
            }
            $audioFile = $this->uploadService->upload($file);
            if (!$audioFile->getPath()) {
                continue;
            }
            $this->parserService->parse($audioFile);
        }
    }
}
