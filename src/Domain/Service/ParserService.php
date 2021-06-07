<?php

declare(strict_types=1);

namespace Genre\Domain\Service;

use Genre\Domain\AudioFile\Entity\AudioFile;
use Genre\Domain\MusicMetrics\Entity\MusicMetrics;
use Genre\Domain\MusicMetrics\Repository\MusicMetricsRepository;

class ParserService
{
    private MusicMetricsRepository $musicMetricsRepository;

    public function __construct(MusicMetricsRepository $musicMetricsRepository)
    {
        $this->musicMetricsRepository = $musicMetricsRepository;
    }

    public function parse(AudioFile $audioFile): MusicMetrics {
        $command = 'python3 /var/www/genre/python/main.py parse ' . $audioFile->getPath();
        $output = null;
        $status = null;
        exec($command, $output, $status);
        $musicMetrics = json_decode($output[0], true);
    }
}
