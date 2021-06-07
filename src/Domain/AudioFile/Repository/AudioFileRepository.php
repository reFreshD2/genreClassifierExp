<?php

namespace Genre\Domain\AudioFile\Repository;

use Doctrine\ORM\EntityManagerInterface;
use Doctrine\ORM\OptimisticLockException;
use Doctrine\ORM\ORMException;
use Genre\Domain\AudioFile\Entity\AudioFile;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;
use Genre\Domain\MusicMetrics\Entity\MusicMetrics;

/**
 * @method AudioFile|null find($id, $lockMode = null, $lockVersion = null)
 * @method AudioFile|null findOneBy(array $criteria, array $orderBy = null)
 * @method AudioFile[]    findAll()
 * @method AudioFile[]    findBy(array $criteria, array $orderBy = null, $limit = null, $offset = null)
 */
class AudioFileRepository extends ServiceEntityRepository
{
    private EntityManagerInterface $entityManager;

    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, AudioFile::class);
        $this->entityManager = $this->getEntityManager();
    }

    /**
     * @throws OptimisticLockException
     * @throws ORMException
     */
    public function save(AudioFile $audioFile): void
    {
        $this->entityManager->persist($audioFile);
        $this->entityManager->flush();
    }
}
