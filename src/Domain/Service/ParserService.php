<?php

declare(strict_types=1);

namespace Genre\Domain\Service;

use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Genre\Domain\AudioFile\Entity\AudioFile;
use Genre\Domain\AudioFile\Repository\AudioFileRepository;
use Genre\Domain\MusicMetrics\Entity\MusicMetrics;
use Genre\Domain\MusicMetrics\Repository\MusicMetricsRepository;

class ParserService
{
    private MusicMetricsRepository $musicMetricsRepository;
    private AudioFileRepository $audioFileRepository;

    public function __construct(
        MusicMetricsRepository $musicMetricsRepository,
        AudioFileRepository $audioFileRepository
    ) {
        $this->musicMetricsRepository = $musicMetricsRepository;
        $this->audioFileRepository = $audioFileRepository;
    }

    /**
     * @throws OptimisticLockException
     * @throws ORMException
     */
    public function parse(AudioFile $audioFile): MusicMetrics {
        // СУПЕРМЕГАКОСТЫЛЬ, не делать так !!!
        $command = "echo 12345 | su - root -s /bin/bash -c 'python3 /var/www/genre/python/main.py parse " . $audioFile->getPath() . "'";
        $output = null;
        $status = null;
        exec($command, $output, $status);

        $musicMetricsArray = json_decode($output[0], true);
        $musicMetrics = MusicMetrics::createFromArray($musicMetricsArray);
        $musicMetrics->setAudioFile($audioFile);
        $this->musicMetricsRepository->save($musicMetrics);
        $audioFile->setMusicMetrics($musicMetrics);
        $this->audioFileRepository->save($audioFile);

        return $musicMetrics;
    }
}
