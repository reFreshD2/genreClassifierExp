<?php

declare(strict_types=1);

namespace Genre\Domain\Service;

use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Genre\Domain\AudioFile\Entity\AudioFile;
use Genre\Domain\AudioFile\Repository\AudioFileRepository;
use Symfony\Component\HttpFoundation\File\UploadedFile;

class UploadService
{
    private string $uploadDir;
    private AudioFileRepository $audioFileRepository;

    public function __construct(string $uploadDir, AudioFileRepository $audioFileRepository)
    {
        $this->uploadDir = $uploadDir;
        $this->audioFileRepository = $audioFileRepository;
    }

    /**
     * @throws OptimisticLockException
     * @throws ORMException
     */
    public function upload(UploadedFile $file): ?AudioFile {
        // хэш не нужен
        $hash = '123';
        if ($this->audioFileRepository->findOneBy(['hash' => $hash])) {
            return null;
        }
        $name = md5($file->getClientOriginalName() . 'Md5F47wn53eoZ3d');
        $audioFile = new AudioFile($this->uploadDir . $name . ".wav", $hash);
        $file->move($this->uploadDir, "$name.wav");
        $this->audioFileRepository->save($audioFile);
        return $audioFile;
    }
}
